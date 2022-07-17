import logging
from utils.aws.s3 import MockS3


class TestS3_Buckets:
    bucket_name = "demo-bucket"

    @classmethod
    def setup_class(cls):
        logging.info("setup_class")

        MockS3.createBucket(cls.bucket_name)

    @classmethod
    def teardown_class(cls):
        logging.info("teardown_class")
        MockS3.garbageCollection(cls.bucket_name)

    def test_sqs_insert(self):
        assert 1 != 1
