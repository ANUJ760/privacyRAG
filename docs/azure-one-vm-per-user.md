# Azure One VM Per User

This mode gives every user or customer their own isolated VM, Ollama runtime,
uploaded files, and ChromaDB volume.

It is simpler than multi-tenant auth/database isolation, but be precise about
the privacy claim:

- If the VM is in the user's Azure subscription, the user controls the data.
- If the VM is in your Azure subscription, users are isolated from each other,
  but you can still technically access the VM as the Azure account owner.

## Recommended Use

Use this for demos, pilots, or customer-owned deployments where each customer
gets a separate instance:

```text
User A -> VM A -> Ollama A -> upload_data A -> chroma_data A
User B -> VM B -> Ollama B -> upload_data B -> chroma_data B
```

## Budget Notes

With a small credit balance, do not leave many VMs running. CPU-only local LLMs
can be slow, and larger VMs burn credits quickly. Stop and deallocate unused VMs
so Azure stops billing for allocated compute. Managed disks and public IPs can
still have small costs.

For a first trial, start with one low-cost Ubuntu VM and the default
`llama3.2:3b` model. Scale up only if responses are too slow.

## Azure Resources Per User

Create one resource group per user/customer:

```text
privacyrag-<user>
```

Each resource group should contain:

- one Ubuntu VM
- one OS disk
- one public IP
- one network security group
- optional larger managed data disk for uploads and ChromaDB

Open inbound ports:

```text
22    SSH, restrict to your IP if possible
3000  frontend
8000  backend API
```

For production, put HTTPS in front of the app and avoid exposing raw port `8000`.

## VM Setup

SSH into the new VM, then run the setup script from the repository.

```bash
git clone <your-repo-url> privacyRAG
cd privacyRAG
```

Run:

```bash
REPO_URL=<your-repo-url> \
PUBLIC_HOST=<vm-public-ip-or-domain> \
MODEL_NAME=llama3.2:3b \
bash scripts/setup-azure-single-tenant-vm.sh
```

Open:

```text
http://<vm-public-ip-or-domain>:3000
```

Health check:

```text
http://<vm-public-ip-or-domain>:8000/health
```

## Add More Models

On that user's VM:

```bash
ollama pull mistral:7b
```

Edit `.env`:

```text
MODEL_NAME=llama3.2:3b
AVAILABLE_MODELS=llama3.2:3b,mistral:7b
```

Restart:

```bash
docker compose up -d --build
```

## Delete A User Instance

When a trial ends, delete the user's resource group in Azure. That removes the
VM, public IP, disks, uploaded files, and ChromaDB data for that instance.

## Next Hardening Steps

- Add HTTPS with a domain and reverse proxy.
- Restrict SSH to your IP address.
- Use Azure Cost Management budgets and alerts.
- Use VM auto-shutdown for demos.
- Add backup only if users explicitly want retention.
- Add a clear privacy notice explaining who controls the VM.
