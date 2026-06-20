from database.supabase import get_supabase_client


def insert_cashflow_entry(data: dict):
    supabase = get_supabase_client()

    response = (
        supabase
        .table("cashflow_entries")
        .insert(data)
        .execute()
    )

    return response


def get_all_cashflow_entries():
    supabase = get_supabase_client()

    response = (
        supabase
        .table("cashflow_entries")
        .select("*")
        .order("period_start", desc=False)
        .execute()
    )

    return response.data


def get_latest_cashflow_entry():
    entries = get_all_cashflow_entries()

    if not entries:
        return None

    return entries[-1]