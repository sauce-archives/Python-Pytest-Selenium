import pytest


@pytest.mark.usefixtures("driver")
def test_add_and_remove_from_cart(driver):
    driver.get('https://www.saucedemo.com/inventory.html')
    driver.find_element_by_class_name('add-to-cart-button').click()
    driver.find_element_by_class_name('add-to-cart-button').click()
    driver.find_element_by_class_name('remove-from-cart-button').click()

    assert driver.find_element_by_class_name('shopping_cart_badge').text == '1'

    driver.get('https://www.saucedemo.com/cart.html')
    expected = driver.find_elements_by_class_name('inventory_item_name')
    assert len(expected) == 1
