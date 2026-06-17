create table if not exists net_worth_snapshots (
    id uuid primary key default gen_random_uuid(),
    snapshot_date date not null,

    bank_balance numeric default 0,
    savings_balance numeric default 0,
    investments_value numeric default 0,
    crypto_value numeric default 0,
    pension_value numeric default 0,
    business_cash numeric default 0,
    other_assets numeric default 0,

    student_debt numeric default 0,
    credit_card_debt numeric default 0,
    loans numeric default 0,
    tax_debt numeric default 0,
    other_debt numeric default 0,

    notes text,
    created_at timestamp with time zone default now()
);