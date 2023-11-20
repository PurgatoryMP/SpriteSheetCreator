class ScriptGenerator:
    """
    A class for generating scripts to animate the sprite sheet.
    """

    def generate_unreal_script(self):
        """
        Generate a blue print script for unreal.
        """
        # TODO find out a useful way to do this.
        script = """"""
        return script

    def generate_pygame_script(self):
        """
        Generate a simple pygame script.
        """
        script = """import pygame
import sys

# Initialize Pygame
pygame.init()

# Function to load a sprite sheet and return a list of frames
def load_sprite_sheet(file_path, num_rows, num_cols):
    sprite_sheet = pygame.image.load(file_path).convert_alpha()
    sprite_width = sprite_sheet.get_width() // num_cols
    sprite_height = sprite_sheet.get_height() // num_rows

    frames = []
    for row in range(num_rows):
        for col in range(num_cols):
            frame = sprite_sheet.subsurface(pygame.Rect(col * sprite_width, row * sprite_height, sprite_width, sprite_height))
            frames.append(frame)

    return frames

def main():
    # Set up display
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Sprite Sheet Animation')

    # Load sprite sheet
    sprite_sheet_path = 'your_sprite_sheet.png'  # Change this to the path of your sprite sheet
    frames = load_sprite_sheet(sprite_sheet_path, 8, 8)  # Adjust the dimensions based on your sprite sheet

    # Set up animation parameters
    frame_index = 0
    frame_delay = 100  # milliseconds per frame
    last_frame_time = pygame.time.get_ticks()

    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update animation frame
        current_time = pygame.time.get_ticks()
        if current_time - last_frame_time >= frame_delay:
            frame_index = (frame_index + 1) % len(frames)
            last_frame_time = current_time

        # Draw current frame
        screen.fill((255, 255, 255))  # White background
        screen.blit(frames[frame_index], (100, 100))  # Adjust the position as needed

        # Update display
        pygame.display.flip()

if __name__ == "__main__":
    main()
"""
        return script

    def generate_godot_script(self):
        """
        Generate a script for godot
        """
        script = """extends AnimatedSprite

# Set the number of columns and rows in your sprite sheet
var sheet_columns = 8
var sheet_rows = 8

# Set the total number of frames in the sprite sheet
var total_frames = sheet_columns * sheet_rows

# Set the animation speed (frames per second)
var animation_speed = 10

# Set the current frame
var current_frame = 0

# Set the time each frame should be displayed
var frame_duration = 1.0 / animation_speed

# Timer for animation
var timer = Timer.new()

func _ready():
    # Connect the timeout signal of the timer to the animation function
    timer.connect("timeout", self, "_on_timeout")

    # Set the timer's wait time
    timer.wait_time = frame_duration

    # Start the timer
    timer.start()

func _process(delta):
    # Calculate the current column and row of the sprite sheet
    var current_column = current_frame % sheet_columns
    var current_row = current_frame // sheet_columns

    # Calculate the width and height of each frame in the sprite sheet
    var frame_width = 1.0 / sheet_columns
    var frame_height = 1.0 / sheet_rows

    # Set the frame coordinates in the sprite sheet
    self.frame_coords = Rect2(current_column * frame_width, current_row * frame_height, frame_width, frame_height)

# Function called on timer timeout
func _on_timeout():
    # Increment the current frame
    current_frame += 1

    # Loop back to the first frame if we've reached the end
    if current_frame >= total_frames:
        current_frame = 0

    # Set the timer's wait time
    timer.wait_time = frame_duration

    # Update the animation frame
    update()
"""
        return script

    def generate_Unity_script(self):
        """
        Generates a basic C# script for unity.
        """
        script = """using UnityEngine;

public class SpriteSheetAnimator : MonoBehaviour
{
    public Texture2D spriteSheet;
    public int rows = 8; // Number of rows in the sprite sheet
    public int columns = 8; // Number of columns in the sprite sheet
    public int framesPerSecond = 12; // Speed of animation

    private SpriteRenderer spriteRenderer;
    private int currentFrame = 0;

    void Start()
    {
        spriteRenderer = GetComponent<SpriteRenderer>();
        InvokeRepeating("NextFrame", 1f / framesPerSecond, 1f / framesPerSecond);
    }

    void NextFrame()
    {
        currentFrame = (currentFrame + 1) % (rows * columns);

        int row = currentFrame / columns;
        int col = currentFrame % columns;

        float width = 1f / columns;
        float height = 1f / rows;

        Vector2 offset = new Vector2(col * width, 1 - height - row * height);

        spriteRenderer.material.SetTextureOffset("_MainTex", offset);
        spriteRenderer.material.SetTextureScale("_MainTex", new Vector2(width, height));
    }
}
        """
        return script

    def generate_lsl_script_option_1(self) -> str:
        """
        Generates a lsl script with all the required parameters.
        """
        script = """integer animOn = TRUE; //Set to FALSE and call initAnim() again to stop the animation.
//Effect parameters: (can be put in list together, to make animation have all of said effects)
//LOOP - loops the animation
//SMOOTH - plays animation smoothly
//REVERSE - plays animation in reverse
//PING_PONG - plays animation in one direction, then cycles in the opposite direction
list effects = [LOOP];
integer movement = 0;
integer link_number = 2;//Number representing the link number that this animation will be played on.
integer face = ALL_SIDES; //Number representing the side to activate the animation on.
integer sideX = 1; //Represents how many horizontal images (frames) are contained in your texture.
integer sideY = 1; //Same as sideX, except represents vertical images (frames).
float start = 0.0; //Frame to start animation on. (0 to start at the first frame of the texture)
float length = 0.0; //Number of frames to animate, set to 0 to animate all frames.
float speed = 10.0; //Frames per second to play.

reset()
{
    llSetLinkTextureAnim(link_number,FALSE, face, 0, 0, 0.0, 0.0, 1.0); // V2 - remove all anims
}

animate()
{
    if(animOn)
    {
        integer effectBits;
        integer i;
        for(i = 0; i < llGetListLength(effects); i++)
        {
            effectBits = (effectBits | llList2Integer(effects,i));
        }
        integer params = (effectBits|movement);
        llSetLinkTextureAnim(link_number, ANIM_ON|params,face,sideX,sideY,     start,length,speed);
    }
    else
    {
        llSetLinkTextureAnim(link_number,0,face,sideX,sideY, start,length,speed);
    }
}

fetch()
{
    string texture = llGetInventoryName(INVENTORY_TEXTURE,0);
    llSetLinkTexture(link_number,texture,face);

    list data  = llParseString2List(texture,["_"],[]);

    llOwnerSay( llDumpList2String(data ,","));

    string anim_state = llList2String(data,0);
    string sprite_sheet_number = llList2String(data,1);
    string rows = llList2String(data,2);
    string columns = llList2String(data,3);
    string frame_count = llList2String(data,4);
    string frame_rate = llList2String(data,5);

    // llOwnerSay("X=" + X + " Y=" + Y + " Z = " + (string) Z);

    sideX = (integer) rows;
    sideY = (integer) columns;
    speed = (float) frame_rate;

    if(speed)
    {
        animate();
    }
}

default
{
    state_entry()
    {
        reset();
        fetch();
    }
    changed(integer change)
    {
        if (change & CHANGED_INVENTORY)
        {
            reset();
            fetch();
        }
    }
}       
        """
        return script

    def generate_lsl_script_option_2(self):

        script = """//Writen by Dantia Gothly 2023
//Version 2.0

//The expected texture name format = spritename_maptype_sequencenumber_rows_columns_framecount_framerate 
// Example: Fireball_defuse_000_8_8_64_24

float timer_rate = 0.002;       // Rate of the timer event
integer link_number = 0;        // The link number of the prim this texture is animated on.
integer face = 0;               // Face of the prim to apply the texture

list defuse_sprite_sheets;      // List to store the names of inventory items
list normal_sprite_sheets;      // List to store the names of inventory items
list specular_sprite_sheets;    // List to store the names of inventory items
integer defuse_list_length;     // The length of the defuse list.
integer normal_list_length;     // The length of the normal list.
integer specular_list_length;   // The length of the specular list.
integer inventory_count;        // Number of inventory items
string inventory_name;          // Name of the current inventory item
integer image_size = 1024;      // Size of the image, this should be left as is.
float image_rotation = 0.0;     // Rotation of the image
string sheet_name;              // Name of the image sheet
integer current_frame;          // Counter for the timer event
integer start_frame;            // Starting frame for animation
integer end_frame;              // Ending frame for animation
integer frame_count;            // Number of frames per image
integer frame_rate;             // Frame rate of the animation
integer sequence_number;        // Current sequence number
integer index;                  // Current index in the inventory loop
integer type;                   // Type of inventory item
integer grid_rows;              // Number of rows in the grid
integer grid_columns;           // Number of columns in the grid

integer load_inventory()
{
    //Load the invnetory into memeory and set the images on the links and faces.
    
    // Set the type to INVENTORY_TEXTURE
    type = INVENTORY_TEXTURE;
    
    // Get the number of inventory items of type INVENTORY_TEXTURE
    inventory_count = llGetInventoryNumber(type);
    
    if(inventory_count != 0) 
    
        // Loop through each inventory item   
        for(index=0 ; index < inventory_count ; index++)
        {
            // Get the name of the inventory item at the current index            
            inventory_name = llGetInventoryName(type, index);
            
            list parse = llParseString2List(inventory_name, ["_"], [""]);
            string map_type = llToLower(llList2String(parse,1));
            
            // Append the inventory name to the inventory list for each material type.            
            if(map_type == "defuse")
            {
                defuse_sprite_sheets = defuse_sprite_sheets + inventory_name;
            }
            else if(map_type == "normal")
            {
                normal_sprite_sheets = normal_sprite_sheets + inventory_name;
            }
            else if(map_type == "specular")
            {
                specular_sprite_sheets = specular_sprite_sheets + inventory_name;
            }    
        }
        
        defuse_list_length = llGetListLength(defuse_sprite_sheets);
        normal_list_length = llGetListLength(normal_sprite_sheets);
        specular_list_length = llGetListLength(specular_sprite_sheets);
        
        // Set the texture of the prim's face to the first image
        llSetLinkPrimitiveParamsFast(link_number,[ PRIM_TEXTURE, face,  llList2String(defuse_sprite_sheets,0), <1.0, 1.0, 0.0>, <0,0,0>, 0.0 ]);
        if(defuse_list_length == normal_list_length == specular_list_length)
        {
             llSetLinkPrimitiveParamsFast(link_number,[ PRIM_NORMAL, face,  llList2String(normal_sprite_sheets,0), <1.0, 1.0, 0.0>, <0,0,0>, 0.0 ]);
             llSetLinkPrimitiveParamsFast(link_number,[ PRIM_SPECULAR, face,  llList2String(specular_sprite_sheets,0), <1.0, 1.0, 0.0>, <0,0,0>, 0.0, <0,0,0>, 51, 0 ]);
        }
        
        // Split the first image string into a list using "_" as the delimiter
        list data  = llParseString2List(llList2String(defuse_sprite_sheets,0),["_"],[]);
        
        // Extract the relevant information from the data list
        sheet_name = llList2String(data,0);
        //map_type = llList2String(data, 1);
        sequence_number = (integer)llList2String(data,2);
        grid_rows = (integer)llList2String(data,3);
        grid_columns = (integer)llList2String(data,4);
        frame_count = (integer)llList2String(data,5);
        frame_rate = (integer)llList2String(data,6);
        start_frame = 0;
        end_frame = frame_count * llGetListLength(defuse_sprite_sheets);

        // Return TRUE to indicate successful loading of inventory
        return TRUE;
}


animate_textures(integer link, integer frame_number)
{
    // Set the texture parameters for the specified link number
    llSetLinkPrimitiveParamsFast(link, [
        PRIM_TEXTURE, face, llList2String(defuse_sprite_sheets,sequence_number), <1,1,0>, <1,1,1>, image_rotation,
        PRIM_NORMAL, face, llList2String(normal_sprite_sheets, sequence_number), <1,1,0>, <1,1,1>,image_rotation,
        PRIM_SPECULAR, face, llList2String(specular_sprite_sheets, sequence_number), <1,1,0>, <1,1,1>,  image_rotation, <1,1,1>, 51, 0]);  
    //Animate The texture.              
    llSetLinkTextureAnim(link, ANIM_ON, face, grid_columns, grid_rows, frame_number, 1, 1);
}

run_loop()
{
    //Loop through each frame of each sprite sheet and then start from the beginning.
    current_frame++;
    sequence_number = current_frame / frame_count;
    if (current_frame >= end_frame) 
    {
        sequence_number = 0;
        current_frame = 0;
    }
    
    animate_textures(link_number, current_frame);       
}

default
{
    state_entry()
    {
        if (load_inventory())
        {
            llSetTimerEvent(timer_rate);
        }        
    }
    timer()
    {
        run_loop();       
    }
}
        """
        return script
