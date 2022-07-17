import logging
import json

from utils.aws.lambda_ import MockLambda


class TestLambda_Invokes:
    fn_name = "test-lambda-fn"

    @classmethod
    def setup_class(cls):
        logging.info("setup_class")

    @classmethod
    def teardown_class(cls):
        logging.info("teardown_class")

    def test_lambda_invoke(self):
        resp = MockLambda.invoke(
            function_name=self.fn_name, payload={"demo": "a", "testing": "b"}
        )
        print(json.loads(resp["Payload"].read()))
        assert 1 != 1
