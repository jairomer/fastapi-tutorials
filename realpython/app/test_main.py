from fastapi.testclient import TestClient

from .main import app 
from .main import Item
from .main import TaxedItem

client = TestClient(app)

def test_get_hello_world():
    response = client.get("/helloworld")
    assert response.status_code == 200
    assert response.json() == "Hello World"

def test_read_item_parameter_happy_path():
    response = client.get("/items/integer/1")
    assert response.status_code == 200
    assert response.json() == {"item_id": 1}

def test_read_item_parameter_invalid_parameter():
    response = client.get("/items/integer/a")
    assert response.status_code == 422 # 422 Unprocessable Entity
    parsed_response = response.json()
    # This is why you make tests, this msg is a misalignment with what the tutorial says
    # should be happening.
    expected_msg = "Input should be a valid integer, unable to parse string as an integer"
    assert parsed_response["detail"][0]["msg"] == expected_msg

def test_create_complete_item():
    new_item = Item(
            name = "Foo",
            price = 1.0,
            description = "An optional description",
            tax = 3.5
            )

    response = client.post(url="/items", content=new_item.model_dump_json())
    assert response.status_code == 200

    received_item = Item.model_validate_json(response.content)
    assert received_item == new_item 

def test_create_basic_item():
   new_item = Item(
           name = "Foo",
           price = 1.0,
           )

   response = client.post(url="/items", content=new_item.model_dump_json())
   assert response.status_code == 200

   received_item = Item.model_validate_json(response.content)
   assert received_item == new_item 

def test_create_complete_taxed_item():
    new_item = Item(
            name = "Foo",
            price = 1.0,
            description = "An optional description",
            tax = 3.5
            )

    response = client.post(url="/items/tax", content=new_item.model_dump_json())
    assert response.status_code == 200

    # If we modify the item with a new attribute, we will need to define it in
    # the schema. Otherwise deserializaton will only get the attributes defined
    # In the original type.
    # This is why we define 'TaxedItem' as a subclass of Item to define this new field.
    received_item = TaxedItem.model_validate_json(response.content)
    print(received_item)
    assert new_item.tax is not None
    assert received_item.price_with_tax == (new_item.price + new_item.tax)


def test_put_complete_item():
    new_item = Item(
            name = "Foo",
            price = 1.0,
            description = "An optional description",
            tax = 3.5
            )

    response = client.put(url="/items/1", content=new_item.model_dump_json())
    assert response.status_code == 200
    # Receive a JSON instead of a concrete typed response.
    received_json = response.json() 
    assert received_json["item_id"] == 1
    assert received_json["name"] == "Foo"
    assert received_json["price"] == 1.0
    assert received_json["tax"] == 3.5
    assert received_json["description"] == "An optional description"
