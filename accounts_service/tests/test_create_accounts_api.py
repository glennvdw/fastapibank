import pytest
from fastapi.testclient import TestClient
from app import app
from dependencies import get_accounts_repository, get_customers_repository
from repositories.accounts_impl_memory import InMemoryAccountsRepository
from repositories.customers_impl_memory import InMemoryCustomersRepository
from models import Customer

def override_accounts_repository():
    return InMemoryAccountsRepository()

def override_customers_repository():
    repository = InMemoryCustomersRepository()
    repository.save(customer=Customer(id="cust-001", name="tester", surname="tester"))
    return repository

@pytest.fixture
def client():
    # Override the global dependency, to create a fresh repo for each test:
    app.dependency_overrides[get_accounts_repository] = override_accounts_repository
    app.dependency_overrides[get_customers_repository] = override_customers_repository
    with TestClient(app) as c:
        yield c
    # Clean up overrides
    app.dependency_overrides.clear()

def test_create_account(client):
    # act
    create_res = client.post(
        "/accounts/", 
        json={"customer_id": "cust-001", "name": "test account"}
    )

    # assert
    assert create_res.status_code == 200
    created_data = create_res.json()
    assert created_data["customer_id"] == "cust-001"
    assert created_data["name"] == "test account"
    assert created_data["balance"] == 0.0

