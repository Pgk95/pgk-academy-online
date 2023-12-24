from flask import render_template, Blueprint, request, flash, url_for, redirect
from flask_login import login_required, current_user
from .models import db
from PIL import Image, ImageDraw

# create the blueprint
profile = Blueprint('profile', __name__)

# define the route


@profile.route('/profile', methods=['GET', 'POST'])
@login_required
def profile_page():
    return render_template('profile.html', user=current_user.username)


@profile.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def upload_picture():
    """Upload a profile picture."""
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
            flash('Profile picture updated!', category='success')
            return redirect(url_for('profile.profile_page'))
    return render_template('edit_profile.html', user=current_user.username)

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
