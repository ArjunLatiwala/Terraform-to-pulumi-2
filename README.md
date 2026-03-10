# Terraform → Pulumi Migration: S3 Static Website

Migrated an AWS S3 static website from Terraform to Pulumi.  
Original project forked from [N4si/simple-terraform-project](https://github.com/N4si/simple-terraform-project).

---

## What This Project Does

Deploys a **static website on AWS S3** with public access, originally written in Terraform, now fully managed by Pulumi.

**AWS Resources:**
- S3 Bucket
- Bucket Ownership Controls
- Bucket Public Access Block
- Bucket ACL (public-read)
- Bucket Website Configuration
- S3 Objects (`index.html`, `error.html`, `profile.png`)

---

## Step 1: Clone & Deploy with Terraform

```bash
git clone https://github.com/N4si/simple-terraform-project.git
cd simple-terraform-project
```

Fix the bucket name in `variables.tf` (S3 bucket names are globally unique):
```hcl
variable "bucketname" {
  default = "your-unique-bucket-name-2026"
}
```

```bash
terraform init
terraform apply
```

---

## Step 2: Convert to Pulumi

```bash
pulumi convert --from terraform --language python --out pulumi-infra
cd pulumi-infra
```

Install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Copy static files into Pulumi folder:
```bash
cp ../index.html .
cp ../error.html .
cp ../profile.png .
```

---

## Step 3: Initialize Pulumi Stack

```bash
pulumi login --local
pulumi stack init dev
pulumi config set aws:region us-east-1
```

---

## Step 4: Import Existing AWS Resources

Create `import.json`:
```json
{
  "resources": [
    { "type": "aws:s3/bucket:Bucket", "name": "mybucket", "id": "your-bucket-name" },
    { "type": "aws:s3/bucketOwnershipControls:BucketOwnershipControls", "name": "example", "id": "your-bucket-name" },
    { "type": "aws:s3/bucketPublicAccessBlock:BucketPublicAccessBlock", "name": "example", "id": "your-bucket-name" },
    { "type": "aws:s3/bucketAclV2:BucketAclV2", "name": "example", "id": "your-bucket-name" },
    { "type": "aws:s3/bucketWebsiteConfigurationV2:BucketWebsiteConfigurationV2", "name": "website", "id": "your-bucket-name" }
  ]
}
```

```bash
pulumi import --file import.json
```

---

## Step 5: Preview & Apply

```bash
pulumi preview
pulumi up
```

---

## Step 6: Remove from Terraform State

```bash
cd ..
terraform state rm aws_s3_bucket.mybucket
terraform state rm aws_s3_bucket_ownership_controls.example
terraform state rm aws_s3_bucket_public_access_block.example
terraform state rm aws_s3_bucket_acl.example
terraform state rm aws_s3_bucket_website_configuration.website
terraform state rm aws_s3_object.index
terraform state rm aws_s3_object.error
terraform state rm aws_s3_object.profile
```

---

## ✅ Outcome

Pulumi is now the single source of truth. The static website is live at:
```
http://your-bucket-name.s3-website-us-east-1.amazonaws.com
```

> ⚠️ Never run `terraform destroy` after migration — use `pulumi down` instead.
