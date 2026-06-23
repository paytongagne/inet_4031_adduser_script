import unittest

from provision_users import build_useradd_command, parse_user_record, shell_join


class TestProvisionUsers(unittest.TestCase):
    def test_parse_valid_user_with_single_group(self):
        record = parse_user_record("user04:pass04:Last04:First04:group01")

        self.assertEqual(record.username, "user04")
        self.assertEqual(record.full_name, "First04 Last04")
        self.assertEqual(record.groups, ["group01"])

    def test_parse_valid_user_with_multiple_groups(self):
        record = parse_user_record("user06:pass06:Last06:First06:group01,group02")

        self.assertEqual(record.groups, ["group01", "group02"])

    def test_parse_user_with_no_group(self):
        record = parse_user_record("user07:pass07:Last07:First07:-")

        self.assertEqual(record.groups, [])

    def test_ignore_comments_and_blank_lines(self):
        self.assertIsNone(parse_user_record("# comment"))
        self.assertIsNone(parse_user_record("   "))

    def test_reject_malformed_record(self):
        with self.assertRaises(ValueError):
            parse_user_record("user09:Last09:First09:group09")

    def test_build_useradd_command(self):
        record = parse_user_record("user04:pass04:Last04:First04:group01")
        command = build_useradd_command(record)

        self.assertEqual(
            command,
            ["sudo", "useradd", "-m", "-c", "First04 Last04", "-G", "group01", "user04"],
        )

    def test_shell_join_quotes_full_name(self):
        record = parse_user_record("user04:pass04:Last04:First04:group01")
        command = shell_join(build_useradd_command(record))

        self.assertIn("'First04 Last04'", command)


if __name__ == "__main__":
    unittest.main()
