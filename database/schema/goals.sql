create table if not exists goals (
    id uuid primary key default gen_random_uuid(),

    goal_name text not null,
    goal_category text not null,

    target_amount numeric(14,2) not null,
    current_amount numeric(14,2) default 0,

    deadline date,
    priority integer default 3,
    status text default 'Active',

    notes text,

    created_at timestamp with time zone default now()
);

alter table goals disable row level security;