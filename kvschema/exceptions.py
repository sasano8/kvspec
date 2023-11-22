class AppProblem(Exception):
    media_type: str = "application/problem+json"
    status: int = 500

    def __init__(
        self, type: str, title: str = "", detail: str = "", instance: str = None
    ):
        """RFC7807に準拠したエラーを表現する

        Parameters
        * type: APIのドキュメンテーション等にリンクするURI
        * title: エラーの簡潔な説明
        * status: HTTPステータスコード
        * detail: エラーの詳細な説明
        * instance: 問題が発生した特定のインスタンスを参照するURI
        """
        self.type = type
        self.title = title
        self.detail = detail
        self.instance = instance

    def to_dict(self):
        return {
            "status": self.status,
            "type": self.type,
            "title": self.title,
            "detail": self.detail,
            "instance": self.instance,
        }

    def get_sample(self):
        return {
            "status": 500,
            "type": "https://yourhost.com/problems/internal-server-error",
            "title": "Internal Server Error",
            "detail": "Error an occurred.",
            "instance": "/account/12345/msgs/abc",
        }
