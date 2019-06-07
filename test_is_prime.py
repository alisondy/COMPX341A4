from unittest import TestCase

from app import is_prime


class TestIsPrime(TestCase):
    def test_isPrime_positive(self):
        self.assertTrue(is_prime(5))

    def test_isPrime_negative(self):
        self.assertFalse(is_prime(6))
