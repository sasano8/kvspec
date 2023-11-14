def test_get_text():
    return

    from gql import gql, Client
    from gql.transport.requests import RequestsHTTPTransport

    transport = RequestsHTTPTransport(
        url="https://localhost/graphql",
        use_json=True,
    )

    # クライアントの作成
    client = Client(
        transport=transport,
        fetch_schema_from_transport=True,
    )

    # 実行するGraphQLクエリ
    query = gql(
        """
        query {
            yourQuery {
                field1
                field2
            }
        }
    """
    )

    # クエリの実行
    result = client.execute(query)
    print(result)
