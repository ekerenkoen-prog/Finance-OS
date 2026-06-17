from database.supabase import get_supabase_client


def insert_net_worth_snapshot(data: dict):
    supabase = get_supabase_client()

    response = (
        supabase
        .table("net_worth_snapshots")
        .insert(data)
        .execute()
    )

    return response


def get_all_snapshots():
    supabase = get_supabase_client()

    response = (
        supabase
        .table("net_worth_snapshots")
        .select("*")
        .order("snapshot_date")
        .execute()
    )

    return response.data


def get_latest_snapshot():
    supabase = get_supabase_client()

    response = (
        supabase
        .table("net_worth_snapshots")
        .select("*")
        .order("snapshot_date", desc=True)
        .limit(1)
        .execute()
    )

    if response.data:
        return response.data[0]

    return None