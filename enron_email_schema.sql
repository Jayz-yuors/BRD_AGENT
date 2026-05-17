CREATE TABLE enron_emails (
    id SERIAL PRIMARY KEY,
    message_id TEXT,
    email_date TIMESTAMP,
    sender TEXT,
    receiver TEXT,
    subject TEXT,
    body TEXT
);