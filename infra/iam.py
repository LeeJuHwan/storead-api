import pulumi
import pulumi_aws as aws


def create_s3_full_access_iam_user():
    iam_user = aws.iam.User("iam_user", name="storead-s3")

    s3_full_access_group = aws.iam.Group("s3_full_access_group", name="s3_full_access_group")

    aws.iam.GroupPolicyAttachment(
        "group_policy_attachment",
        group=s3_full_access_group.name,
        policy_arn="arn:aws:iam::aws:policy/AmazonS3FullAccess",
    )

    aws.iam.UserGroupMembership("group_membership", user=iam_user.name, groups=[s3_full_access_group.name])

    iam_profile = aws.iam.UserLoginProfile("iam_profile", user=iam_user.name, password_reset_required=True)

    access_key = aws.iam.AccessKey("user_access_key", user=iam_user.name, status="Active")

    pulumi.export("iam_user_name", iam_user.name)
    pulumi.export("iam_user_password", iam_profile.password)
    pulumi.export("iam_user_access_key", access_key.id)

    # NOTE: CLI -> pulumi stack output iam_user_secret_key --show-secrets로 Secret block 내용 확인 가능
    pulumi.export("iam_user_secret_key", access_key.secret)
    return iam_user
