def behandel_sp_list_page(item, session=None, page=None):

    from q_haderslev_vbo.automation_server.ats_update_item_data import update_item_data
    from q_haderslev_vbo.automation_server.ats_find_state import find_state
    from q_sharepoint_api.functionality.sp_list_item_ats_box import (
        create_or_update_from_ats_box,
        get_to_ats_box
    )

    import logging
    logger = logging.getLogger(__name__)

    data = item.data

    # ---------------------------------------------------------
    # STATES
    # ---------------------------------------------------------
    class States:
        CREATE = "1.0 Created in SharePoint"
        GET = "2.0 Hentet fra SharePoint"
        UPDATE = "3.0 Opdateret i SharePoint"

    def har_state(state):
        return find_state(data, search_text=state)

    def set_state(state):
        update_item_data(data, item=item, state=state)

    def log(step, text):
        logger.info(f"[{step}] {text}")

    # =========================================================
    # STEP 1 – CREATE
    # =========================================================
    state = States.CREATE

    if har_state(state) is False:

        log("CREATE", "Opretter i SharePoint")

        create_or_update_from_ats_box(
            site_name="Automatisering",
            list_name="Test - Rune",
            item=item,
            robot_kommentar="Created via ATS test"
        )

        update_item_data(data, item=item)
        set_state(state)

    # =========================================================
    # STEP 2 – GET
    # =========================================================
    state = States.GET

    if har_state(state) is False:

        log("GET", "Henter fra SharePoint")

        get_to_ats_box(
            site_name="Automatisering",
            list_name="Test - Rune",
            list_item_id=data["box"]["sharepoint"]["id"],
            item=item
        )

        update_item_data(data, item=item)
        set_state(state)

    # =========================================================
    # STEP 3 – UPDATE
    # =========================================================
    state = States.UPDATE

    if har_state(state) is False:

        log("UPDATE", "Opdaterer SharePoint")

        # 🔧 ændring
        gammel = data["box"]["sharepoint"]["Beløb"]
        data["box"]["sharepoint"]["Beløb"] = gammel + 50

        create_or_update_from_ats_box(
            site_name="Automatisering",
            list_name="Test - Rune",
            item=item,
            robot_kommentar="Updated via ATS test"
        )

        update_item_data(data, item=item)
        set_state(state)