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
        .order("snapshot_date", desc=False)
        .execute()
    )

    return response.data


def get_latest_snapshot():
    snapshots = get_all_snapshots()

    if not snapshots:
        return None

    return snapshots[-1]