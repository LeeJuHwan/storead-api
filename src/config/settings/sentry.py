from config.env import ENV

SENTRY_DSN = ENV.str("SENTRY_DSN", default="")

if SENTRY_DSN:
    environment = ENV("SENTRY_ENVIRONMENT", default="dev")

    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        send_default_pii=True,
        # NITE: 1.0 to capture 100%
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        environment=environment,
        release="storead-api@0.1.0",
    )
