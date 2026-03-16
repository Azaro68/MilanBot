CREATE TABLE IF NOT EXISTS subscribers (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL UNIQUE,
    chat_id BIGINT NOT NULL,
    username TEXT,
    first_name TEXT,
    subscribed_at TIMESTAMPTZ,
    is_subscription_active BOOLEAN NOT NULL DEFAULT FALSE,
    is_bot_chat_active BOOLEAN NOT NULL DEFAULT TRUE,
    welcome_sent_at TIMESTAMPTZ,
    last_random_sent_at TIMESTAMPTZ,
    last_fixed_sent_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_subscribers_active
    ON subscribers (is_subscription_active);

CREATE INDEX IF NOT EXISTS idx_subscribers_last_random
    ON subscribers (last_random_sent_at);

CREATE INDEX IF NOT EXISTS idx_subscribers_last_fixed
    ON subscribers (last_fixed_sent_at);
