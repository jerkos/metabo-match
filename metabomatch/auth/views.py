# -*- coding: utf-8 -*-
"""
    auth.views
    This view provides user authentication, registration and a view for
    resetting the password of a user if he has lost his password

"""
from flask import Blueprint, flash, redirect, url_for, request, current_app, session
from flask.ext.login import (current_user, login_user, login_required,
                             logout_user, confirm_login, login_fresh)

from metabomatch.extensions import github
from metabomatch.flaskbb.utils.helpers import render_template
from metabomatch.email import send_reset_token
from metabomatch.auth.forms import (LoginForm, ReauthForm, ForgotPasswordForm, ResetPasswordForm)
from metabomatch.user.models import User


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    Logs the user in
    """

    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for("user.profile"))

    form = LoginForm(request.form)
    if form.validate_on_submit():
        user, authenticated = User.authenticate(form.login.data,
                                                form.password.data)

        if user and authenticated:
            #remove this key when a user is authenticated
            session.pop('nb_views', None)
            login_user(user, remember=form.remember_me.data)
            return redirect(request.args.get("next") or url_for("home.index"))

        flash("Wrong username or password", "danger")
    return render_template("auth/login.html", form=form)


@auth.route("/reauth", methods=["GET", "POST"])
@login_required
def reauth():
    """
    Reauthenticates a user
    """

    if not login_fresh():
        form = ReauthForm(request.form)
        if form.validate_on_submit():
            confirm_login()
            flash("Reauthenticated", "success")
            return redirect(request.args.get("next") or
                            url_for("user.profile"))
        return render_template("auth/reauth.html", form=form)
    return redirect(request.args.get("next") or
                    url_for("user.profile", username=current_user.username))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out", "success")
    return redirect(url_for("home.index"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    """
    Register a new user
    """

    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for("user.profile"))

    if current_app.config["RECAPTCHA_ENABLED"]:
        from metabomatch.auth.forms import RegisterRecaptchaForm
        form = RegisterRecaptchaForm(request.form)
    else:
        from metabomatch.auth.forms import RegisterForm
        form = RegisterForm(request.form)

    if form.validate_on_submit():
        user = form.save()
        login_user(user)

        flash("Thanks for registering", "success")
        return redirect(url_for("user.profile", username=current_user.username))
    return render_template("auth/register.html", form=form)


@auth.route('/resetpassword', methods=["GET", "POST"])
def forgot_password():
    """
    Sends a reset password token to the user.
    """

    if not current_user.is_anonymous():
        return redirect(url_for("forum.index"))

    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            token = user.make_reset_token()
            send_reset_token(user, token=token)

            flash("E-Mail sent! Please check your inbox.", "info")
            return redirect(url_for("auth.forgot_password"))
        else:
            flash(("You have entered an username or email that is not linked \
                with your account"), "danger")
    return render_template("auth/forgot_password.html", form=form)


@auth.route("/resetpassword/<token>", methods=["GET", "POST"])
def reset_password(token):
    """
    Handles the reset password process.
    """

    if not current_user.is_anonymous():
        return redirect(url_for("forum.index"))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        expired, invalid, data = user.verify_reset_token(form.token.data)

        if invalid:
            flash("Your password token is invalid.", "danger")
            return redirect(url_for("auth.forgot_password"))

        if expired:
            flash("Your password is expired.", "danger")
            return redirect(url_for("auth.forgot_password"))

        if user and data:
            user.password = form.password.data
            user.save()
            flash("Your password has been updated.", "success")
            return redirect(url_for("auth.login"))

    form.token.data = token
    return render_template("auth/reset_password.html", form=form)


#  github authentication
@auth.route("/login_github")
def login_github():
    return github.authorize()


@auth.route('/github-callback')
@github.authorized_handler
def authorized(oauth_token):
    #next_url = request.args.get('next') or url_for('index')
    if oauth_token is None:
        flash("Authorization failed.", "danger")
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(github_access_token=oauth_token).first()
    if user is None:
        user = User.create_github_account(oauth_token)

    if user is None:
        flash("An error occurred during github auth.", "danger")
        return redirect(url_for('auth.login'))

    session.pop('nb_views', None)
    #  force remembering
    login_user(user, True)
    flash("Github oauth succeeded.", "success")

    return redirect(url_for('softwares.index'))


@github.access_token_getter
def token_getter():
    #token = User.options(load_only("id", "github_access_token")).filter(User.id == 1).first()
    #return token[1]
    u = User.query.filter(User.id == 1).first()
    return u.github_access_token
