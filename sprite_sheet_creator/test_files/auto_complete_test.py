import sys
from PyQt5.QtGui import QTextCursor, QTextCharFormat
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QCompleter
from PyQt5.QtCore import Qt


class ScriptingIDE(QMainWindow):
    def __init__(self):
        super().__init__()

        self.script_editor = None
        self.setWindowTitle('Scripting IDE')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # Create a custom widget that includes QTextEdit and QCompleter
        self.script_editor = ScriptEditor(self)
        layout.addWidget(self.script_editor)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


class ScriptEditor(QTextEdit):
    def __init__(self, parent):
        super().__init__(parent)

        # Add autocomplete functionality
        self.words_to_highlight = None
        self._completer = None
        self.highlighting = None
        self.setupAutocomplete()

    def setupAutocomplete(self):
        # Sample word list for autocomplete
        self.words_to_highlight = ["if", "else", "for", "while", "TRUE", "FALSE", "llAbs", "llAcos",
                                   "llAddToLandBanList", "llAddToLandPassList", "llAdjustSoundVolume",
                                   "llAgentInExperience", "llAllowInventoryDrop", "llAngleBetween", "llApplyImpulse",
                                   "llApplyRotationalImpulse", "llAsin", "llAtan2", "llAttachToAvatar",
                                   "llAttachToAvatarTemp", "llAvatarOnLinkSitTarget", "llAvatarOnSitTarget",
                                   "llAxes2Rot", "llAxisAngle2Rot", "llBase64ToInteger", "llBase64ToString",
                                   "llBreakAllLinks", "llBreakLink", "llCastRay", "llCeil", "llChar",
                                   "llClearCameraParams", "llClearLinkMedia", "llClearPrimMedia",
                                   "llCloseRemoteDataChannel", "llCloud", "llCollisionFilter", "llCollisionSound",
                                   "llCollisionSprite", "llCos", "llCreateCharacter", "llCreateKeyValue",
                                   "llCreateLink", "llCSV2List", "llDataSizeKeyValue", "llDeleteCharacter",
                                   "llDeleteKeyValue", "llDeleteSubList", "llDeleteSubString", "llDetachFromAvatar",
                                   "llDetectedGrab", "llDetectedGroup", "llDetectedKey", "llDetectedLinkNumber",
                                   "llDetectedName", "llDetectedOwner", "llDetectedPos", "llDetectedRot",
                                   "llDetectedTouchBinormal", "llDetectedTouchFace", "llDetectedTouchNormal",
                                   "llDetectedTouchPos", "llDetectedTouchST", "llDetectedTouchUV", "llDetectedType",
                                   "llDetectedVel", "llDialog", "llDie", "llDumpList2String", "llEdgeOfWorld",
                                   "llEjectFromLand", "llEmail", "llEscapeURL", "llEuler2Rot", "llEvade",
                                   "llExecCharacterCmd", "llFabs", "llFleeFrom", "llFloor", "llForceMouselook",
                                   "llFrand", "llGenerateKey", "llGetAccel", "llGetAgentInfo", "llGetAgentLanguage",
                                   "llGetAgentList", "llGetAgentSize", "llGetAlpha", "llGetAndResetTime",
                                   "llGetAnimation", "llGetAnimationList", "llGetAnimationOverride", "llGetAttached",
                                   "llGetAttachedList", "llGetBoundingBox", "llGetCameraPos", "llGetCameraRot",
                                   "llGetCenterOfMass", "llGetClosestNavPoint", "llGetColor", "llGetCreator",
                                   "llGetDate", "llGetDayLength", "llGetDayOffset", "llGetDisplayName", "llGetEnergy",
                                   "llGetEnv", "llGetEnvironment", "llGetExperienceDetails",
                                   "llGetExperienceErrorMessage", "llGetForce", "llGetFreeMemory", "llGetFreeURLs",
                                   "llGetGeometricCenter", "llGetGMTclock", "llGetHTTPHeader",
                                   "llGetInventoryAcquireTime", "llGetInventoryCreator", "llGetInventoryKey",
                                   "llGetInventoryName", "llGetInventoryNumber", "llGetInventoryPermMask",
                                   "llGetInventoryType", "llGetKey", "llGetLandOwnerAt", "llGetLinkKey",
                                   "llGetLinkMedia", "llGetLinkName", "llGetLinkNumber", "llGetLinkNumberOfSides",
                                   "llGetLinkPrimitiveParams", "llGetListEntryType", "llGetListLength", "llGetLocalPos",
                                   "llGetLocalRot", "llGetMass", "llGetMassMKS", "llGetMaxScaleFactor",
                                   "llGetMemoryLimit", "llGetMinScaleFactor", "llGetMoonDirection", "llGetMoonRotation",
                                   "llGetNextEmail", "llGetNotecardLine", "llGetNumberOfNotecardLines",
                                   "llGetNumberOfPrims", "llGetNumberOfSides", "llGetObjectAnimationNames",
                                   "llGetObjectDesc", "llGetObjectDetails", "llGetObjectLinkKey", "llGetObjectMass",
                                   "llGetObjectName", "llGetObjectPermMask", "llGetObjectPrimCount", "llGetOmega",
                                   "llGetOwner", "llGetOwnerKey", "llGetParcelDetails", "llGetParcelFlags",
                                   "llGetParcelMaxPrims", "llGetParcelMusicURL", "llGetParcelPrimCount",
                                   "llGetParcelPrimOwners", "llGetPermissions", "llGetPermissionsKey",
                                   "llGetPhysicsMaterial", "llGetPos", "llGetPrimitiveParams", "llGetPrimMediaParams",
                                   "llGetRegionAgentCount", "llGetRegionCorner", "llGetRegionDayLength",
                                   "llGetRegionDayOffset", "llGetRegionFlags", "llGetRegionFPS",
                                   "llGetRegionMoonDirection", "llGetRegionMoonRotation", "llGetRegionName",
                                   "llGetRegionSunDirection", "llGetRegionSunRotation", "llGetRegionTimeDilation",
                                   "llGetRootPosition", "llGetRootRotation", "llGetRot", "llGetScale",
                                   "llGetScriptName", "llGetScriptState", "llGetSimStats", "llGetSimulatorHostname",
                                   "llGetSPMaxMemory", "llGetStartParameter", "llGetStaticPath", "llGetStatus",
                                   "llGetSubString", "llGetSunDirection", "llGetSunRotation", "llGetTexture",
                                   "llGetTextureOffset", "llGetTextureRot", "llGetTextureScale", "llGetTime",
                                   "llGetTimeOfDay", "llGetTimestamp", "llGetTorque", "llGetUnixTime",
                                   "llGetUsedMemory", "llGetUsername", "llGetVel", "|llGetVisualParams",
                                   "llGetWallclock", "llGiveInventory", "llGiveInventoryList", "llGiveMoney",
                                   "llGodLikeRezObject", "llGround", "llGroundContour", "llGroundNormal",
                                   "llGroundRepel", "llGroundSlope", "llHash", "llHMAC", "llHTTPRequest",
                                   "llHTTPResponse", "llInsertString", "llInstantMessage", "llIntegerToBase64",
                                   "llIsFriend", "llJson2List", "llJsonGetValue", "llJsonSetValue", "llJsonValueType",
                                   "llKey2Name", "llKeyCountKeyValue", "llKeysKeyValue", "llLinear2sRGB",
                                   "llLinkAdjustSoundVolume", "llLinkParticleSystem", "llLinkPlaySound",
                                   "llLinksetDataAvailable", "llLinksetDataCountFound", "llLinksetDataCountKeys",
                                   "llLinksetDataDelete", "llLinksetDataDeleteFound", "llLinksetDataDeleteProtected",
                                   "llLinksetDataFindKeys", "llLinksetDataListKeys", "llLinksetDataRead",
                                   "llLinksetDataReadProtected", "llLinksetDataReset", "llLinksetDataWrite",
                                   "llLinksetDataWriteProtected", "llLinkSetSoundQueueing", "llLinkSetSoundRadius",
                                   "llLinkSitTarget", "llLinkStopSound", "llList2CSV", "llList2Float", "llList2Integer",
                                   "llList2Json", "llList2Key", "llList2List", "llList2ListSlice", "llList2ListStrided",
                                   "llList2Rot", "llList2String", "llList2Vector", "llListen", "llListenControl",
                                   "llListenRemove", "llListFindList", "llListFindListNext", "llListFindStrided",
                                   "llListInsertList", "llListRandomize", "llListReplaceList", "llListSort",
                                   "llListSortStrided", "llListStatistics", "llLoadURL", "llLog", "llLog10", "llLookAt",
                                   "llLoopSound", "llLoopSoundMaster", "llLoopSoundSlave", "llMakeExplosion",
                                   "llMakeFire", "llMakeFountain", "llMakeSmoke", "llManageEstateAccess",
                                   "llMapDestination", "llMD5String", "llMessageLinked", "llMinEventDelay",
                                   "llModifyLand", "llModPow", "llMoveToTarget", "llName2Key", "llNavigateTo",
                                   "llOffsetTexture", "llOpenFloater", "llOpenRemoteDataChannel", "llOrd",
                                   "llOverMyLand", "llOwnerSay", "llParcelMediaCommandList", "llParcelMediaQuery",
                                   "llParseString2List", "llParseStringKeepNulls", "llParticleSystem",
                                   "llPassCollisions", "llPassTouches", "llPatrolPoints", "llPlaySound",
                                   "llPlaySoundSlave", "llPointAt", "llPow", "llPreloadSound", "llPursue",
                                   "llPushObject", "llReadKeyValue", "llRefreshPrimURL", "llRegionSay", "llRegionSayTo",
                                   "llReleaseCamera", "llReleaseControls", "llReleaseURL", "llRemoteDataReply",
                                   "llRemoteDataSetRegion", "llRemoteLoadScript", "llRemoteLoadScriptPin",
                                   "llRemoveFromLandBanList", "llRemoveFromLandPassList", "llRemoveInventory",
                                   "llRemoveVehicleFlags", "llReplaceAgentEnvironment", "llReplaceEnvironment",
                                   "llReplaceSubString", "llRequestAgentData", "llRequestDisplayName",
                                   "llRequestExperiencePermissions", "llRequestInventoryData", "llRequestPermissions",
                                   "llRequestSecureURL", "llRequestSimulatorData", "llRequestURL", "llRequestUserKey",
                                   "llRequestUsername", "llResetAnimationOverride", "llResetLandBanList",
                                   "llResetLandPassList", "llResetOtherScript", "llResetScript", "llResetTime",
                                   "llReturnObjectsByID", "llReturnObjectsByOwner", "llRezAtRoot", "llRezObject",
                                   "llRezObjectWithParams", "llRot2Angle", "llRot2Axis", "llRot2Euler", "llRot2Fwd",
                                   "llRot2Left", "llRot2Up", "llRotateTexture", "llRotBetween", "llRotLookAt",
                                   "llRotTarget", "llRotTargetRemove", "llRound", "llSameGroup", "llSay",
                                   "llScaleByFactor", "llScaleTexture", "llScriptDanger", "llScriptProfiler",
                                   "llSendRemoteData", "llSensor", "llSensorRemove", "llSensorRepeat",
                                   "llSetAgentEnvironment", "llSetAlpha", "llSetAngularVelocity",
                                   "llSetAnimationOverride", "llSetBuoyancy", "llSetCameraAtOffset",
                                   "llSetCameraEyeOffset", "llSetCameraParams", "llSetClickAction", "llSetColor",
                                   "llSetContentType", "llSetDamage", "llSetEnvironment", "llSetForce",
                                   "llSetForceAndTorque", "llSetHoverHeight", "llSetInventoryPermMask",
                                   "llSetKeyframedMotion", "llSetLinkAlpha", "llSetLinkCamera", "llSetLinkColor",
                                   "llSetLinkMedia", "llSetLinkPrimitiveParams", "llSetLinkPrimitiveParamsFast",
                                   "llSetLinkTexture", "llSetLinkTextureAnim", "llSetLocalRot", "llSetMemoryLimit",
                                   "llSetObjectDesc", "llSetObjectName", "llSetObjectPermMask", "llSetParcelMusicURL",
                                   "llSetPayPrice", "llSetPhysicsMaterial", "llSetPos", "llSetPrimitiveParams",
                                   "llSetPrimMediaParams", "llSetPrimURL", "llSetRegionPos",
                                   "llSetRemoteScriptAccessPin", "llSetRot", "llSetScale", "llSetScriptState",
                                   "llSetSitText", "llSetSoundQueueing", "llSetSoundRadius", "llSetStatus", "llSetText",
                                   "llSetTexture", "llSetTextureAnim", "llSetTimerEvent", "llSetTorque",
                                   "llSetTouchText", "llSetVehicleFlags", "llSetVehicleFloatParam",
                                   "llSetVehicleRotationParam", "llSetVehicleType", "llSetVehicleVectorParam",
                                   "llSetVelocity", "llSHA1String", "llSHA256String", "llShout", "llSignRSA", "llSin",
                                   "llSitOnLink", "llSitTarget", "llSleep", "llSound", "llSoundPreload", "llSqrt",
                                   "llsRGB2Linear", "llStartAnimation", "llStartObjectAnimation", "llStopAnimation",
                                   "llStopObjectAnimation", "llStopHover", "llStopLookAt", "llStopMoveToTarget",
                                   "llStopPointAt", "llStopSound", "llStringLength", "llStringToBase64", "llStringTrim",
                                   "llSubStringIndex", "llTakeCamera", "llTakeControls", "llTan", "llTarget",
                                   "llTargetedEmail", "llTargetOmega", "llTargetRemove", "llTeleportAgent",
                                   "llTeleportAgentGlobalCoords", "llTeleportAgentHome", "llTextBox", "llToLower",
                                   "llToUpper", "llTransferLindenDollars", "llTriggerSound", "llTriggerSoundLimited",
                                   "llUnescapeURL", "llUnSit", "llUpdateCharacter", "llUpdateKeyValue", "llVecDist",
                                   "llVecMag", "llVecNorm", "llVerifyRSA", "llVolumeDetect", "llWanderWithin",
                                   "llWater", "llWhisper", "llWind", "llXorBase64", "llXorBase64Strings",
                                   "llXorBase64StringsCorrect", "attach()", "at_rot_target()", "at_target()",
                                   "changed()", "collision()",
                                   "collision_end()", "collision_start()", "control()", "dataserver()", "email()",
                                   "event_order()",
                                   "experience_permissions()", "experience_permissions_denied()", "game_control()",
                                   "http_request()",
                                   "http_response()", "land_collision()", "land_collision_end()",
                                   "land_collision_start()",
                                   "linkset_data()", "link_message()", "listen()", "money()", "moving_end()",
                                   "moving_start()",
                                   "not_at_rot_target()", "not_at_target()", "no_sensor()", "object_rez()", "on_rez()",
                                   "path_update()", "remote_data()", "run_time_permissions()", "sensor()",
                                   "state_entry()",
                                   "state_exit()", "timer()", "touch()", "touch_end()", "touch_start()",
                                   "transaction_result()",
                                   "string", "list", "vector", "rotation", "key", "float", "PI_BY_TWO", "PI", "TWO_PI",
                                   "RAD_TO_DEG"]

        completer = QCompleter(self.words_to_highlight, self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)

        # Set the QCompleter for the QTextEdit
        self.setCompleter(completer)

        # Set up a flag to prevent recursion
        self.highlighting = False

    def setCompleter(self, completer):
        self._completer = completer
        self._completer.setWidget(self)
        self._completer.activated.connect(self.insertCompletion)

    def insertCompletion(self, completion):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, len(self._completer.completionPrefix()))
        cursor.insertText(completion)
        self._completer.popup().hide()

    def textUnderCursor(self):
        cursor = self.textCursor()
        cursor.select(QTextCursor.WordUnderCursor)
        return cursor.selectedText()

    def keyPressEvent(self, event):
        if self._completer.popup().isVisible():
            if event.key() in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Escape, Qt.Key_Tab, Qt.Key_Backtab):
                event.ignore()
                return

        super().keyPressEvent(event)
        completion_prefix = self.textUnderCursor()

        if len(completion_prefix) < 1:
            self._completer.popup().hide()
            return

        if completion_prefix != self._completer.completionPrefix():
            self._completer.setCompletionPrefix(completion_prefix)
            popup = self._completer.popup()
            popup.setCurrentIndex(self._completer.completionModel().index(0, 0))

            cr = self.cursorRect()
            cr.setWidth(self._completer.popup().sizeHintForColumn(0)
                        + self._completer.popup().verticalScrollBar().sizeHint().width())
            self._completer.complete(cr)  # popup it up!

            # Update the highlighting
            self.update_highlight()

    def update_highlight(self):
        if not self.highlighting:
            # Set the flag to indicate highlighting is in progress
            self.highlighting = True

            try:
                # Clear previous formatting
                cursor = self.textCursor()
                cursor.select(QTextCursor.Document)
                cursor.setCharFormat(QTextCharFormat())
                cursor.clearSelection()

                # Highlight each word in the list in red
                document = self.document()
                for word_to_highlight in self._completer.model().stringList():
                    cursor = QTextCursor(document)
                    format_highlight = QTextCharFormat()
                    format_highlight.setForeground(Qt.red)

                    # Search for the word and apply formatting
                    while not cursor.isNull() and not cursor.atEnd():
                        cursor = document.find(word_to_highlight, cursor)
                        if cursor.isNull():
                            break
                        cursor.mergeCharFormat(format_highlight)

            except Exception as e:
                print(f"Error during highlighting: {e}")

            finally:
                # Reset the flag
                self.highlighting = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ide = ScriptingIDE()
    ide.show()
    sys.exit(app.exec_())
