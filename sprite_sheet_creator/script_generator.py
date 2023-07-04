class ScriptGenerator():
    """
    A class for generating scripts to animate the sprite sheet.
    """

    # TODO: Create scripts that support the following:
    #  LSL:
    #   llTextureAnimation()
    #   llSetLinkPrimitiveParamsFast()
    #  Python: for TK and QT5
    #  GDScript
    #  C# for unity
    #  C++ for Unreal.

    def __init__(self):
        pass

    def generate_lsl_script_option_1(self) -> str:
        """
        Generates a lsl script with all the required parameters.
        """

        values = {}

        script = """        
            integer animOn = TRUE; //Set to FALSE and call initAnim() again to stop the animation.
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
        """ % values
        return script

    def generate_lsl_script_option_2(self):

        script = """
            //Writen by Dantia Gothly 2023
            //Version 1.0
            
            //The expected texture name format = spritename_maptype_sequencenumber_rows_columns_framecount_framerate
            
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
            float frame_horizontal_size;    // Width of each frame
            float frame_vertical_size;      // Height of each frame
            float horizontal_repeats;       // Number of horizontal repeats for the texture
            float vertical_repeats;         // Number of vertical repeats for the texture
            vector repeats;                 // Repeats vector for the texture
            
            integer has_materials;          // Indicates that normals and specular sprite sheets were added.
            
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
                    llSetLinkPrimitiveParamsFast(0,[ PRIM_TEXTURE, face,  llList2String(defuse_sprite_sheets,0), <1.0, 1.0, 0.0>, <0,0,0>, 0.0 ]);
                    if(defuse_list_length == normal_list_length == specular_list_length)
                    {
                         llSetLinkPrimitiveParamsFast(0,[ PRIM_NORMAL, face,  llList2String(normal_sprite_sheets,0), <1.0, 1.0, 0.0>, <0,0,0>, 0.0 ]);
                         llSetLinkPrimitiveParamsFast(0,[ PRIM_SPECULAR, face,  llList2String(specular_sprite_sheets,0), <1.0, 1.0, 0.0>, <0,0,0>, 0.0, <0,0,0>, 51, 0 ]);
                         has_materials = TRUE;
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
                    
                    //llOwnerSay((string)end_frame);
                    
                    // Calculate the size of each frame
                    frame_horizontal_size = (float)image_size / grid_columns;
                    frame_vertical_size = (float)image_size / grid_rows;
                    
                    // Calculate the number of horizontal and vertical repeats for the texture
                    horizontal_repeats = frame_horizontal_size / image_size;
                    vertical_repeats = frame_vertical_size / image_size;    
                    repeats = <horizontal_repeats, vertical_repeats, 0>;
                    
                    // Return TRUE to indicate successful loading of inventory
                    return TRUE;
            }
            
            
            animate_texture(integer link, string defuse_texture, integer frame_number)
            {
                // This function animates a texture on a specific face of a prim
                
                // Calculate the grid index based on the frame number and the grid size
                integer grid_index = frame_number % (grid_rows * grid_columns);
                
                // Calculate the row and column of the current frame in the grid
                integer row = grid_index / grid_columns;
                integer col = grid_index % grid_columns;
                
                // Calculate the horizontal and vertical offsets for the current frame
                float frame_horizontal_offset = ((float)col + 0.5) / grid_columns - 0.5;
                float frame_vertical_offset = ((float)row + 0.5) / grid_rows - 0.5;
                
                // Create a vector to store the offsets
                vector offsets = <frame_horizontal_offset, -frame_vertical_offset, 0.0>;
                
                // Set the texture parameters for the specified link number
                llSetLinkPrimitiveParamsFast(link, [PRIM_TEXTURE, face, defuse_texture, repeats, offsets, image_rotation]);
            }
            
            
            animate_textures(integer link, string defuse_texture, string normal_texture, string specular_texture, integer frame_number)
            {
                // This function animates a texture on a specific face of a prim
                
                // Calculate the grid index based on the frame number and the grid size
                integer grid_index = frame_number % (grid_rows * grid_columns);
                
                // Calculate the row and column of the current frame in the grid
                integer row = grid_index / grid_columns;
                integer col = grid_index % grid_columns;
                
                // Calculate the horizontal and vertical offsets for the current frame
                float frame_horizontal_offset = ((float)col + 0.5) / grid_columns - 0.5;
                float frame_vertical_offset = ((float)row + 0.5) / grid_rows - 0.5;
                
                // Create a vector to store the offsets
                vector offsets = <frame_horizontal_offset, -frame_vertical_offset, 0.0>;
                
                // Set the texture parameters for the specified link number
                llSetLinkPrimitiveParamsFast(link, [
                    PRIM_TEXTURE, face, defuse_texture, repeats, offsets, image_rotation,
                    PRIM_NORMAL, face, normal_texture, repeats, offsets,image_rotation,
                    PRIM_SPECULAR, face, specular_texture, repeats, offsets,  image_rotation, <1,1,1>, 51, 0]);
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
                    current_frame++;
                    sequence_number = current_frame / frame_count;
                    if (current_frame >= end_frame) 
                    {
                        sequence_number = 0;
                        current_frame = 0;
                    }
                    
                    if(has_materials)
                    {
                        animate_textures(
                        link_number,
                        llList2String(defuse_sprite_sheets,sequence_number),
                        llList2String(normal_sprite_sheets, sequence_number),
                        llList2String(specular_sprite_sheets, sequence_number),
                        current_frame);
                    }
                    else
                    {
                        animate_texture(
                        link_number,
                        llList2String(defuse_sprite_sheets, sequence_number),
                        current_frame);
                    }        
                }
            }
        """
        return script
