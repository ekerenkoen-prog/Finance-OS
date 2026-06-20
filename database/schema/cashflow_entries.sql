create table if not exists cashflow_entries (
    id uuid primary key default gen_random_uuid(),

    period_start date not null,
    period_end date not null,

    salary_income numeric(14,2) default 0,
    side_income numeric(14,2) default 0,
    business_income numeric(14,2) default 0,
    dividend_income numeric(14,2) default 0,
    other_income numeric(14,2) default 0,

    housing_expense numeric(14,2) default 0,
    groceries_expense numeric(14,2) default 0,
    eating_out_expense numeric(14,2) default 0,
    transport_expense numeric(14,2) default 0,
    travel_expense numeric(14,2) default 0,
    fun_expense numeric(14,2) default 0,
    other_expense numeric(14,2) default 0,

    invested_amount numeric(14,2) default 0,

    notes text,

    created_at timestamp with time zone default now()
);