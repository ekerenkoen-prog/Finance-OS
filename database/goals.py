from database.supabase import get_supabase_client


def insert_goal(data: dict):
    supabase = get_supabase_client()

    response = (
        supabase
        .table("goals")
        .insert(data)
        .execute()
    )

    return response


def get_all_goals():
    supabase = get_supabase_client()

    response = (
        supabase
        .table("goals")
        .select("*")
        .order("created_at", desc=False)
        .execute()
    )

    return response.data


def get_active_goals():
    goals = get_all_goals()

    return [
        goal for goal in goals
        if goal.get("status") == "Active"
    ]


def get_completed_goals():
    goals = get_all_goals()

    return [
        goal for goal in goals
        if goal.get("status") == "Completed"
    ]

def update_goal(goal_id: str, data: dict):
    supabase = get_supabase_client()

    response = (
        supabase
        .table("goals")
        .update(data)
        .eq("id", goal_id)
        .execute()
    )

    return response