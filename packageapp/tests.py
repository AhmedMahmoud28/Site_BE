import pytest

from packageapp.models import Package


@pytest.mark.django_db
def test_package_model():
    package = Package.objects.create(name="Test Package", price=100)

    assert package.name == "Test Package"
    assert package.price == 100

    assert str(package) == "Test Package"
