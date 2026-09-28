*** Settings ***
Library           SeleniumLibrary

Suite Setup       Open Test Browser
Suite Teardown    Close Browser

*** Variables ***
${URL}             https://the-internet.herokuapp.com/login
${USERNAME}        tomsmith
${PASSWORD}        SuperSecretPassword!
${BROWSER}         chrome

*** Test Cases ***
Verify Successful Login Using Custom Keywords
    [Documentation]    Verify login using reusable custom keywords.
    Open Login Page
    Enter Login Credentials    ${USERNAME}    ${PASSWORD}
    Submit Login Form
    Verify Successful Login
    Capture Page Screenshot    ../screenshots/01_successful_login.png
    Logout From Application
    Capture Page Screenshot    ../screenshots/02_login_after_logout.png

*** Keywords ***
Open Test Browser
    Open Browser    about:blank    ${BROWSER}
    Maximize Browser Window

Open Login Page
    Go To    ${URL}
    Wait Until Element Is Visible    id=username    timeout=10s
    Log    Login page opened successfully.

Enter Login Credentials
    [Arguments]    ${username}    ${password}
    Input Text    id=username    ${username}
    Input Text    id=password    ${password}
    Log    Login credentials entered.

Submit Login Form
    Click Button    css=button[type="submit"]
    Log    Login form submitted.

Verify Successful Login
    Wait Until Page Contains    You logged into a secure area!    timeout=10s
    Page Should Contain    You logged into a secure area!
    Page Should Contain    Secure Area
    Log    Successful login verified.

Logout From Application
    Click Link    Logout
    Wait Until Page Contains    You logged out of the secure area!    timeout=10s
    Page Should Contain    You logged out of the secure area!
    Log    Logout successful.