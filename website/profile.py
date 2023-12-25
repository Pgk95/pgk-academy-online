from flask import render_template, Blueprint, request, flash, url_for, redirect
from flask_login import login_required, current_user
from .models import db, User
from PIL import Image, ImageDraw


# create the blueprint
profile = Blueprint('profile', __name__)

# define the route

# route for the profile page
@profile.route('/profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def profile_page(user_id):
    """Display the profile page."""
    # get the user
    user = User.query.get_or_404(user_id)
    return render_template('profile.html', username=user.username)


# route for the edit profile page
@profile.route('/profile/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def upload_picture(user_id):
    """Upload a profile picture."""
    # get the user id
    user = User.query.get_or_404(user_id)

    try:
        if request.method == 'POST':
            # get the form data
            if 'profile_picture' in request.files:
                picture = request.files['profile_picture']

            # Resize the image before saving
            picture = resize_and_crop_image(picture)

            # save the image
            picture_filename = f"{current_user.id}_profile.jpg"
            picture.save(f"website/static/profile_pics/{picture_filename}")
            current_user.profile_picture = picture_filename
            db.session.commit()
            flash('Profile picture updated successfully!', category='success')
            return redirect(url_for('profile.profile_page', user_id=user.id))
    except Exception as e:
        flash('There was an error updating your profile picture. try checking your file format(jpg, jpeg,)', category='error')
    return render_template('edit_profile.html', username=user.username)


# resizing handler function
def resize_and_crop_image(image):
    """Resize and crop the uploaded image to a circular shape."""
    output_size = (125, 125)
    img = Image.open(image)

   # Convert the image to RGBA mode (if it's not already)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

     # Create the circular thumbnail mask
    thumbnail = img.copy()  # Create a copy of the image for resizing
    thumbnail.thumbnail(output_size)

    mask = Image.new('L', thumbnail.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + output_size, fill=255)

    # Apply the alpha channel from the mask to the thumbnail
    thumbnail.putalpha(mask)

    # Convert the image back to RGB for saving
    thumbnail = thumbnail.convert('RGB')

    return thumbnail


@profile.route('/profile/<int:user_id>/edit/username', methods=['GET', 'POST'])
# function to change the username
def change_username(user_id):
    """Change the username."""
    # get the user
    user = User.query.get_or_404(user_id)

    try:
        if request.method == 'POST':
            # get the form data
            new_username = request.form.get('username')

            # check if the username exists
            username_exists = User.query.filter_by(
                username=new_username).first()

            if username_exists:
                flash('Username is already in use.', category='error')
            else:
                # update the username
                user.username = new_username
                db.session.commit()
                flash('Username updated!', category='success')
                return redirect(url_for('profile.profile_page', user_id=user.id))
    except Exception as e:
        flash('There was an error updating your username.', category='error')
    return render_template('edit_profile.html', username=user.username)
