

class ScriptGenerator():
    def __init__(self):


    def generate_lsl_script(self) -> str:
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
                string collumns = llList2String(data,3);
                string frame_count = llList2String(data,4);
                string frame_rate = llList2String(data,5);
            
                // llOwnerSay("X=" + X + " Y=" + Y + " Z = " + (string) Z);
            
                sideX = (integer) rows;
                sideY = (integer) collumns;
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