search_query = """
    SELECT * FROM production.Video WHERE video_title LIKE '%%(query_string)s%'
"""