import arrow

class HeadersValidator:
    def check_header(self, response):
          expected_date = str(arrow.now().format('ddd, DD MMM YYYY'))
          actual_date = response.headers["date"]
          actual_date = actual_date[0:16]
          assert expected_date == actual_date
          assert len(str(response.headers["etag"])) >= 1
          assert len(str(response.headers["connection"])) >= 1
          assert len(str(response.headers["content-length"])) >= 1
          assert len(str(response.headers["server"])) >= 1
          assert len(str(response.headers["x-frame-options"])) >= 1
          assert len(str(response.headers["x-powered-by"])) >= 1
