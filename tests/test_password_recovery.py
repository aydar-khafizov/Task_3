import allure

from pages.login_page import LoginPage
from pages.forgot_password_page import ForgotPasswordPage
from pages.reset_password_page import ResetPasswordPage


@allure.feature("Восстановление пароля")
class TestPasswordRecovery:

    @allure.title("Переход на страницу восстановления пароля")
    def test_go_to_forgot_password_page(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.click_forgot_password_link()

        forgot_page = ForgotPasswordPage(driver)
        assert forgot_page.is_opened(), "Не открылась страница восстановления пароля"

    @allure.title("Ввод почты и клик по кнопке «Восстановить»")
    def test_submit_email_for_recovery(self, driver, registered_user):
        forgot_page = ForgotPasswordPage(driver)
        forgot_page.open()
        forgot_page.enter_email(registered_user["email"])
        forgot_page.click_restore_button()

        # Ждём, пока SPA переключит URL на /reset-password
        forgot_page.wait_for_url("/reset-password")

        reset_page = ResetPasswordPage(driver)
        assert reset_page.is_opened(), "Не открылась форма ввода нового пароля"

    @allure.title("Клик по кнопке показать/скрыть пароль активирует поле")
    def test_show_hide_password_activates_field(self, driver, registered_user):
        forgot_page = ForgotPasswordPage(driver)
        forgot_page.open()
        forgot_page.enter_email(registered_user["email"])
        forgot_page.click_restore_button()

        forgot_page.wait_for_url("/reset-password")

        reset_page = ResetPasswordPage(driver)
        reset_page.click_show_hide_password()

        assert reset_page.is_password_field_active(), (
            "Поле пароля не подсветилось после клика по «показать/скрыть»"
        )