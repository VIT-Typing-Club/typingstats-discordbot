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
