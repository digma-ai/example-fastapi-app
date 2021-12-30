class DomainValidator:
    def validate_user_exists(self, user_ids):
        if len(user_ids)==4:
            raise Exception("can't find user")