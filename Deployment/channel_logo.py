import os

def get_channel_logo_path(channel_name):
    # logo_dir = r'D:\waqarsahi\smart-media-monitoring-ai\channel_logos'
    logo_dir=r"D:\Forbmax User Data\waqar sahi\smart-media-monitoring-ai\channel_logos"
    logo_file = f'{channel_name}.png'
    logo_path = os.path.join(logo_dir, logo_file)

    if os.path.exists(logo_path):
        return logo_path
    else:
        return None  # Return None if the logo doesn't exist

# # Example usage:
# channel_name = "geo"
# logo_path = get_channel_logo_path(channel_name)
# if logo_path:
#     print(f"The logo for channel '{channel_name}' is located at: {logo_path}")
# else:
#     print(f"No logo found for channel '{channel_name}'")