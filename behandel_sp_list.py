async def behandel_sp_list_page(item, session, page):

    from q_haderslev_vbo.automation_server.ats_update_item_data import update_item_data
    from pprint import pprint
    from q_haderslev_vbo.automation_server.ats_find_state import find_state
    from q_datafordeleren_api.functionality.datafordeler_client import DatafordelerClient
    from q_sharepoint_api.functionality.sp_list_item_ats_box import (
        create_or_update_from_ats_box,
        get_to_ats_box
    )

    import logging
    logger = logging.getLogger(__name__)

    data = item.data
    print("Er inde på behandel_sp_list siden")

    """
    Samme struktur som standard template:
    - step → state → mangler_state
    - log_step
    - set_state
    """

    # ==========================================================
    # 🧠 STATES
    # ==========================================================
    class States:
        GET = "2.0 Hentet fra SharePoint"
        UPDATE = "3.0 Opdateret i SharePoint"

    # ==========================================================
    # 🔁 HELPERS
    # ==========================================================

    def mangler_state(state, step):
        states = data.get("state", [])

        match = next((s for s in states if state in s), None)

        if match:
            log_step(step, f'Skip "{match}"')
            return False

        return True

    def set_state(state):
        update_item_data(data, item=item, state=state)
    
    def log_step(step, text):
        print(f"➡️ [{step}] {text}")


    # ==========================================================
    step = "GET"
    # ==========================================================
    state = getattr(States, step)

    #if mangler_state(state, step):

    log_step(step, "Start")

    get_to_ats_box(
        site_name="Automatisering",
        list_name="Test - Rune",
        list_item_id=data["box"]["sharepoint"]["id"],
        item=item
    )

    update_item_data(data, item=item)

    set_state(state)

    # ==========================================================
    step = "UPDATE"
    # ==========================================================
    state = getattr(States, step)

    if mangler_state(state, step):

        log_step(step, "Start")

        gammel = data["box"]["sharepoint"]["Beløb"]
        data["box"]["sharepoint"]["Beløb"] = gammel + 50
        data["box"]["sharepoint"]["Sagsbehandler - Initialer"] = "Test"
      #  create_or_update_from_ats_box(
      #      site_name="Automatisering",
      #      list_name="Test - Rune",
      #      item=item,
      #      robot_kommentar="Updated via ATS test"
      #  )

        update_item_data(data, item=item)

        set_state(state)

    # ==========================================================
    step = "DATAFORDELER"
    # ==========================================================

    log_step(step, "Start")

    client = DatafordelerClient()

    result = client.get_aktuel_navn_og_adresse(
        data["box"]["sharepoint"]["Title"]
    )

    print("✅ AKTUELT RESULTAT:\n")
    pprint(result, width=120)