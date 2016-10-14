import mechanicalsoup as mechanize

def grab_pds(username, password, institute, pds_url):
    """Using the authentication data, makes a POST call to the PDS
    and returns a token."""
    uat_dps_url = pds_url
    br = mechanize.Browser()
    login_page = br.get(pds_url)
    login_form = login_page.soup.find("form", attrs={"name": "form1"})
    login_form.find("input", attrs={"name":"bor_id"})['value'] = username
    login_form.find("input", attrs={"name": "bor_verification"})['value'] = password
    login_form.find("select", attrs={"name": "institute"})['value'] = institute
    page = br.submit(login_form, login_page.url)
    content = page.text
    pds_start = content.find("pds_handle=") + 11
    pds_end = content.find("&calling_system", pds_start)
    pds_token = content[pds_start:pds_end]
    if len(pds_token) > 40: # chosen because the pds tokens are always shorter
                            # than 40 chars, and anything longer suggests that
                            # we were unable to cleanly retrieve a token.
        raise ValueError("Unable to retrieve token for those credentials")
    return pds_token