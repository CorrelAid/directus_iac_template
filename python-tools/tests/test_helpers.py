from python_tools.helpers import switch_flow, dev_admin_access_token

def test_switch_flow():
    current_status = switch_flow(name="Assign Doctor", access_token=dev_admin_access_token(), status="active")
    assert current_status == "active"
    switch_flow(name="Assign Doctor", access_token=dev_admin_access_token(), status=current_status)
