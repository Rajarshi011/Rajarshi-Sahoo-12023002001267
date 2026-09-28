*** Settings ***
Library    SeleniumLibrary

Suite Setup       Open Test Browser
Suite Teardown    Close Browser
Test Template     Verify Login With Different Credentials

*** Variables ***
${URL}              https://the-internet.herokuapp.com/login
${BROWSER}          chrome
${SCREENSHOT_DIR}   C:/Users/rajar/Desktop/Selenium/screenshots

*** Test Cases ***
Valid Login
    tomsmith    SuperSecretPassword!    You logged into a secure area!    01_valid_login.png

Invalid Username
    wronguser    SuperSecretPassword!    Your username is invalid!    02_invalid_username.png

Invalid Password
    tomsmith    wrongpassword    Your password is invalid!    03_invalid_password.png

*** Keywords ***
Open Test Browser
    Open Browser    about:blank    ${BROWSER}
    Maximize Browser Window

Verify Login With Different Credentials
    [Arguments]    ${username}    ${password}    ${expected_message}    ${screenshot}

    Go To    ${URL}
    Wait Until Element Is Visible    id=username    timeout=10s

    Input Text    id=username    ${username}
    Input Text    id=password    ${password}

    Click Button    css=button[type="submit"]

    Wait Until Page Contains    ${expected_message}    timeout=10s
    Page Should Contain    ${expected_message}

    Capture Page Screenshot    ${SCREENSHOT_DIR}/${screenshot}
    Log    Login test completed for username: ${username}