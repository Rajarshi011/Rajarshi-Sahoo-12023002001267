*** Settings ***
Library    SeleniumLibrary

Suite Setup       Open Test Browser
Suite Teardown    Close Browser

*** Variables ***
${URL}         https://the-internet.herokuapp.com/login
${USERNAME}    tomsmith
${PASSWORD}    SuperSecretPassword!
${BROWSER}     chrome

*** Test Cases ***
Verify Login Page
    [Documentation]    Verify that the login page opens successfully.
    Open Login Page
    Page Should Contain Element    id=username
    Page Should Contain Element    id=password
    Capture Page Screenshot    screenshots/01_login_page.png
    Log    Login page displayed successfully.

Verify Successful Login
    [Documentation]    Verify login using valid credentials.
    Open Login Page
    Input Text    id=username    ${USERNAME}
    Input Text    id=password    ${PASSWORD}
    Capture Page Screenshot    screenshots/02_credentials_entered.png
    Click Button    css=button[type="submit"]
    Wait Until Page Contains    You logged into a secure area!    timeout=10s
    Page Should Contain    You logged into a secure area!
    Capture Page Screenshot    screenshots/03_successful_login.png
    Log    Login successful and verified.

*** Keywords ***
Open Test Browser
    Open Browser    about:blank    ${BROWSER}
    Maximize Browser Window

Open Login Page
    Go To    ${URL}
    Wait Until Element Is Visible    id=username    timeout=10s