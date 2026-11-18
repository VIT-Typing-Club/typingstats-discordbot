async def get_user_daily_scores(db, discord_id: str, days: int = None):

    if days is not None:
        query = """
            SELECT
                s.quote_id,
                s.wpm,
                s.accuracy,
                s.raw,
                s.pp,
                s.created_at,
                q.difficulty
            FROM public.typegg_scores s
            LEFT JOIN public.daily_quotes q
                ON s.quote_id = q.quote_id
            WHERE s.user_id = $1
              AND s.created_at >= NOW() - ($2 * INTERVAL '1 day')
            ORDER BY s.created_at ASC;
        """

        return await db.fetch(query, discord_id, days)

    # all time query
    query = """
        SELECT
            s.quote_id,
            s.wpm,
            s.accuracy,
            s.raw,
            s.pp,
            s.created_at,
            q.difficulty
        FROM public.typegg_scores s
        LEFT JOIN public.daily_quotes q
            ON s.quote_id = q.quote_id
        WHERE s.user_id = $1
        ORDER BY s.created_at ASC;
    """

    return await db.fetch(query, discord_id)

async def get_top_players(db, limit: int = 10):
    query = """
        SELECT
            s.user_id AS discord_id,
            COALESCE(u.displayname, u.username, 'Unknown') AS username,
            SUM(COALESCE(s.pp, 0)) AS total_pp,
            AVG(s.wpm) AS avg_wpm,
        COUNT(*) AS total_scores
        FROM public.typegg_scores s
        LEFT JOIN public.users u
            ON s.user_id = u.discord_id
        GROUP BY
            s.user_id,
            u.displayname,
            u.username
        ORDER BY total_pp DESC
        LIMIT $1;
    """

    return await db.fetch(query, limit)
