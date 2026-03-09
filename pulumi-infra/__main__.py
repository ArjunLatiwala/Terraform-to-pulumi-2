import pulumi
import pulumi_aws as aws

config = pulumi.Config()
bucketname = config.get("bucketname")
if bucketname is None:
    bucketname = "arjunterraformbucket2026"
#create s3 bucket
mybucket = aws.s3.Bucket("mybucket", bucket=bucketname)
example = aws.s3.BucketOwnershipControls("example",
    bucket=mybucket.id,
    rule={
        "object_ownership": "BucketOwnerPreferred",
    })
example_bucket_public_access_block = aws.s3.BucketPublicAccessBlock("example",
    bucket=mybucket.id,
    block_public_acls=False,
    block_public_policy=False,
    ignore_public_acls=False,
    restrict_public_buckets=False)
example_bucket_acl = aws.s3.BucketAcl("example",
    bucket=mybucket.id,
    acl="public-read",
    opts = pulumi.ResourceOptions(depends_on=[
            example,
            example_bucket_public_access_block,
        ]))
index = aws.s3.BucketObjectv2("index",
    bucket=mybucket.id,
    key="index.html",
    source=pulumi.FileAsset("index.html"),
    acl="public-read",
    content_type="text/html",
    opts = pulumi.ResourceOptions(depends_on=[example_bucket_acl]))
error = aws.s3.BucketObjectv2("error",
    bucket=mybucket.id,
    key="error.html",
    source=pulumi.FileAsset("error.html"),
    acl="public-read",
    content_type="text/html",
    opts = pulumi.ResourceOptions(depends_on=[example_bucket_acl]))
profile = aws.s3.BucketObjectv2("profile",
    bucket=mybucket.id,
    key="profile.png",
    source=pulumi.FileAsset("profile.png"),
    acl="public-read",
    opts = pulumi.ResourceOptions(depends_on=[example_bucket_acl]))
website = aws.s3.BucketWebsiteConfiguration("website",
    bucket=mybucket.id,
    index_document={
        "suffix": "index.html",
    },
    error_document={
        "key": "error.html",
    },
    opts = pulumi.ResourceOptions(depends_on=[example_bucket_acl]))
pulumi.export("websiteendpoint", website.website_endpoint)
