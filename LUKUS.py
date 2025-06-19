import gi
gi.require_version('Gtk', '4.0')
import os
import json
import urllib.request
from gi.repository import Gtk, GLib, GdkPixbuf

class LukuWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.set_title("Lukus - Sober FFlags Modifier")
        self.set_default_size(700, 450)

        logo_url = "https://i.postimg.cc/KYg2SKGf/59a711a4-5083-43ac-a1fd-216876fba3e2-removalai-preview.png"
        logo_path = "/tmp/lukus_logo.png"
        try:
            if not os.path.exists(logo_path):
                urllib.request.urlretrieve(logo_url, logo_path)
            logo_picture = Gtk.Picture.new_for_filename(logo_path)
            logo_picture.set_content_fit(Gtk.ContentFit.CONTAIN)
            logo_picture.set_size_request(180, 180)
        except Exception as e:
            print(f"Could not load logo in UI: {e}")

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.set_child(vbox)
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(300)
        switcher = Gtk.StackSwitcher(stack=self.stack)
        vbox.append(switcher)
        vbox.append(self.stack)

        easy_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24, margin_top=30, margin_bottom=30, margin_start=30, margin_end=30)
        if 'logo_picture' in locals():
            easy_box.append(logo_picture)
        label = Gtk.Label(label="WELCOME TO LUKUS")
        label.set_margin_bottom(20)
        label.set_margin_top(20)
        label.set_margin_start(20)
        label.set_margin_end(20)
        easy_box.append(label)
        fps_frame = Gtk.Frame(label="FPS Unlock")
        fps_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12, margin_top=12, margin_bottom=12, margin_start=12, margin_end=12)
        fps_label = Gtk.Label(label="FPS:")
        self.fps_entry = Gtk.Entry(placeholder_text="E.g.: 60")
        self.fps_entry.set_text("")
        fps_box.append(fps_label)
        fps_box.append(self.fps_entry)
        fps_frame.set_child(fps_box)
        easy_box.append(fps_frame)
        occ_frame = Gtk.Frame(label="Occlusion Culling")
        occ_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12, margin_top=12, margin_bottom=12, margin_start=12, margin_end=12)
        occ_label = Gtk.Label(label="Enable")
        self.fflag_occlusion = Gtk.Switch()
        self.fflag_occlusion.set_active(False)
        occ_box.append(occ_label)
        occ_box.append(self.fflag_occlusion)
        occ_frame.set_child(occ_box)
        easy_box.append(occ_frame)
        lighting_frame = Gtk.Frame(label="Lightning Technologies")
        lighting_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12, margin_top=12, margin_bottom=12, margin_start=12, margin_end=12)
        self.switch_voxel = Gtk.Switch()
        self.switch_voxel.set_active(False)
        voxel_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        voxel_row.append(Gtk.Label(label="Voxel Lighting (Phase 1)"))
        voxel_row.append(self.switch_voxel)
        lighting_box.append(voxel_row)
        self.switch_shadow = Gtk.Switch()
        self.switch_shadow.set_active(False)
        shadow_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        shadow_row.append(Gtk.Label(label="Shadowmap Lighting (Phase 2)"))
        shadow_row.append(self.switch_shadow)
        lighting_box.append(shadow_row)
        self.switch_future = Gtk.Switch()
        self.switch_future.set_active(False)
        future_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        future_row.append(Gtk.Label(label="Future Lighting (Phase 3)"))
        future_row.append(self.switch_future)
        lighting_box.append(future_row)
        lighting_frame.set_child(lighting_box)
        easy_box.append(lighting_frame)
        advanced_frame = Gtk.Frame(label="Advanced Graphics")
        advanced_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, margin_top=10, margin_bottom=10, margin_start=10, margin_end=10)
        self.switch_avatar_chat = Gtk.Switch()
        self.switch_avatar_chat.set_active(False)
        avatar_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        avatar_row.append(Gtk.Label(label="Avatar Chat Visualization"))
        avatar_row.append(self.switch_avatar_chat)
        advanced_box.append(avatar_row)
        self.switch_hyper = Gtk.Switch()
        self.switch_hyper.set_active(False)
        hyper_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        hyper_row.append(Gtk.Label(label="HyperThreading"))
        hyper_row.append(self.switch_hyper)
        advanced_box.append(hyper_row)
        max_threads_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        max_threads_row.append(Gtk.Label(label="Maximum Threads:"))
        self.spin_max_threads = Gtk.SpinButton()
        self.spin_max_threads.set_range(1, 9999)
        self.spin_max_threads.set_increments(1, 10)
        self.spin_max_threads.set_value(2400)
        max_threads_row.append(self.spin_max_threads)
        advanced_box.append(max_threads_row)
        min_threads_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        min_threads_row.append(Gtk.Label(label="Minimum Threads:"))
        self.spin_min_threads = Gtk.SpinButton()
        self.spin_min_threads.set_range(1, 100)
        self.spin_min_threads.set_increments(1, 1)
        self.spin_min_threads.set_value(3)
        min_threads_row.append(self.spin_min_threads)
        advanced_box.append(min_threads_row)
        self.switch_smooth_terrain = Gtk.Switch()
        self.switch_smooth_terrain.set_active(False)
        smooth_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        smooth_row.append(Gtk.Label(label="Smoother Terrain"))
        smooth_row.append(self.switch_smooth_terrain)
        advanced_box.append(smooth_row)
        quality_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.switch_quality = Gtk.Switch()
        self.switch_quality.set_active(False)
        quality_row.append(Gtk.Label(label="Graphics Quality Level:"))
        quality_row.append(self.switch_quality)
        self.spin_quality = Gtk.SpinButton()
        self.spin_quality.set_range(1, 10)
        self.spin_quality.set_increments(1, 1)
        self.spin_quality.set_value(1)
        quality_row.append(self.spin_quality)
        advanced_box.append(quality_row)
        terrain_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.switch_terrain = Gtk.Switch()
        self.switch_terrain.set_active(False)
        terrain_row.append(Gtk.Label(label="Low Quality Terrain Textures:"))
        terrain_row.append(self.switch_terrain)
        self.spin_terrain = Gtk.SpinButton()
        self.spin_terrain.set_range(4, 64)
        self.spin_terrain.set_increments(4, 4)
        self.spin_terrain.set_value(4)
        terrain_row.append(self.spin_terrain)
        advanced_box.append(terrain_row)
        self.switch_no_shadows = Gtk.Switch()
        self.switch_no_shadows.set_active(False)
        no_shadows_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        no_shadows_row.append(Gtk.Label(label="Disable Shadows"))
        no_shadows_row.append(self.switch_no_shadows)
        advanced_box.append(no_shadows_row)
        self.switch_dpi = Gtk.Switch()
        self.switch_dpi.set_active(False)
        dpi_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        dpi_row.append(Gtk.Label(label="Preserve rendering quality with display setting"))
        dpi_row.append(self.switch_dpi)
        advanced_box.append(dpi_row)
        self.switch_wind = Gtk.Switch()
        self.switch_wind.set_active(False)
        wind_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        wind_row.append(Gtk.Label(label="Disable Wind"))
        wind_row.append(self.switch_wind)
        advanced_box.append(wind_row)
        self.switch_postfx = Gtk.Switch()
        self.switch_postfx.set_active(False)
        postfx_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        postfx_row.append(Gtk.Label(label="Disable PostFX"))
        postfx_row.append(self.switch_postfx)
        advanced_box.append(postfx_row)
        self.switch_gray_sky = Gtk.Switch()
        self.switch_gray_sky.set_active(False)
        gray_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        gray_row.append(Gtk.Label(label="Gray Sky"))
        gray_row.append(self.switch_gray_sky)
        advanced_box.append(gray_row)
        self.switch_light_atten = Gtk.Switch()
        self.switch_light_atten.set_active(False)
        atten_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        atten_row.append(Gtk.Label(label="Lighting Attenuation"))
        atten_row.append(self.switch_light_atten)
        advanced_box.append(atten_row)
        self.switch_gpu_culling = Gtk.Switch()
        self.switch_gpu_culling.set_active(False)
        gpu_culling_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        gpu_culling_row.append(Gtk.Label(label="Enable GPULightCulling"))
        gpu_culling_row.append(self.switch_gpu_culling)
        advanced_box.append(gpu_culling_row)
        fb_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.switch_fb = Gtk.Switch()
        self.switch_fb.set_active(False)
        fb_row.append(Gtk.Label(label="Frame Buffer:"))
        fb_row.append(self.switch_fb)
        self.spin_fb = Gtk.SpinButton()
        self.spin_fb.set_range(0, 10)
        self.spin_fb.set_increments(1, 1)
        self.spin_fb.set_value(4)
        fb_row.append(self.spin_fb)
        advanced_box.append(fb_row)
        self.switch_high_tex = Gtk.Switch()
        self.switch_high_tex.set_active(False)
        high_tex_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        high_tex_row.append(Gtk.Label(label="High Quality Textures"))
        high_tex_row.append(self.switch_high_tex)
        advanced_box.append(high_tex_row)
        low_tex_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        low_tex_row.append(Gtk.Label(label="Lower Quality Textures:"))
        self.spin_low_tex = Gtk.SpinButton()
        self.spin_low_tex.set_range(-1, 3)
        self.spin_low_tex.set_increments(1, 1)
        self.spin_low_tex.set_value(-1)
        low_tex_row.append(self.spin_low_tex)
        advanced_box.append(low_tex_row)
        self.switch_no_avatar_tex = Gtk.Switch()
        self.switch_no_avatar_tex.set_active(False)
        no_avatar_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        no_avatar_row.append(Gtk.Label(label="No avatar textures"))
        no_avatar_row.append(self.switch_no_avatar_tex)
        advanced_box.append(no_avatar_row)
        self.switch_no_grass = Gtk.Switch()
        self.switch_no_grass.set_active(False)
        no_grass_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        no_grass_row.append(Gtk.Label(label="Remove Grass"))
        no_grass_row.append(self.switch_no_grass)
        advanced_box.append(no_grass_row)
        msaa_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.switch_msaa = Gtk.Switch()
        self.switch_msaa.set_active(False)
        msaa_row.append(Gtk.Label(label="Force MSAA:"))
        msaa_row.append(self.switch_msaa)
        self.spin_msaa = Gtk.SpinButton()
        self.spin_msaa.set_range(0, 16)
        self.spin_msaa.set_increments(1, 1)
        self.spin_msaa.set_value(4)
        msaa_row.append(self.spin_msaa)
        advanced_box.append(msaa_row)
        bias_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.switch_bias = Gtk.Switch()
        self.switch_bias.set_active(False)
        bias_row.append(Gtk.Label(label="ShadowMap Bias:"))
        bias_row.append(self.switch_bias)
        self.spin_bias = Gtk.SpinButton()
        self.spin_bias.set_range(0, 100)
        self.spin_bias.set_increments(1, 1)
        self.spin_bias.set_value(75)
        bias_row.append(self.spin_bias)
        advanced_box.append(bias_row)
        self.switch_outline = Gtk.Switch()
        self.switch_outline.set_active(False)
        outline_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        outline_row.append(Gtk.Label(label="Humanoid Outline"))
        outline_row.append(self.switch_outline)
        advanced_box.append(outline_row)
        self.switch_xray = Gtk.Switch()
        self.switch_xray.set_active(False)
        xray_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        xray_row.append(Gtk.Label(label="Buggy ZPlane Camera (Xray)"))
        xray_row.append(self.switch_xray)
        advanced_box.append(xray_row)
        advanced_frame.set_child(advanced_box)
        easy_box.append(advanced_frame)
        apply_btn = Gtk.Button(label="Apply settings")
        apply_btn.connect("clicked", self.on_apply_easy)
        easy_box.append(apply_btn)
        easy_scroll = Gtk.ScrolledWindow()
        easy_scroll.set_child(easy_box)
        easy_scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.stack.add_titled(easy_scroll, "easy", "Easy Access")
        fflags_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8, margin_top=12, margin_bottom=12, margin_start=12, margin_end=12)
        self.config_path = os.path.expanduser("~/.var/app/org.vinegarhq.Sober/config/sober/config.json")
        sober_dir = os.path.dirname(self.config_path)
        if not os.path.exists(sober_dir):
            dialog = Gtk.MessageDialog(transient_for=self, modal=True, buttons=Gtk.ButtonsType.CLOSE, message_type=Gtk.MessageType.ERROR, text="Sober folder not found!\nStart Sober at least once.")
            dialog.connect("response", lambda d, r: d.destroy())
            dialog.present()
        self.path_label = Gtk.Label(label=f"Config: {self.config_path}")
        self.path_label.set_xalign(0)
        fflags_box.append(self.path_label)
        entry_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.fflag_entry = Gtk.Entry(placeholder_text="FFlag name")
        self.value_entry = Gtk.Entry(placeholder_text="Value (true/false/text)")
        entry_box.append(self.fflag_entry)
        entry_box.append(self.value_entry)
        fflags_box.append(entry_box)
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        add_button = Gtk.Button(label="Add FFlag")
        add_button.connect("clicked", self.on_add_fflag)
        remove_button = Gtk.Button(label="Remove Selected")
        remove_button.connect("clicked", self.on_remove_fflag)
        save_button = Gtk.Button(label="Save FFlags")
        save_button.connect("clicked", self.on_save_fflags)
        import_button = Gtk.Button(label="Import FFlags from .json")
        import_button.connect("clicked", self.on_import_fflags)
        clear_button = Gtk.Button(label="Delete All Flags")
        clear_button.connect("clicked", self.on_clear_fflags)
        button_box.append(add_button)
        button_box.append(remove_button)
        button_box.append(save_button)
        button_box.append(import_button)
        button_box.append(clear_button)
        fflags_box.append(button_box)
        self.fflag_store = Gtk.ListStore(str, str)
        self.fflag_view = Gtk.TreeView(model=self.fflag_store)
        renderer_fflag = Gtk.CellRendererText()
        renderer_fflag.set_property("editable", True)
        renderer_fflag.connect("edited", self.on_fflag_edited, 0)
        column_fflag = Gtk.TreeViewColumn("FFlag", renderer_fflag, text=0)
        self.fflag_view.append_column(column_fflag)
        renderer_value = Gtk.CellRendererText()
        renderer_value.set_property("editable", True)
        renderer_value.connect("edited", self.on_fflag_edited, 1)
        column_value = Gtk.TreeViewColumn("Value", renderer_value, text=1)
        self.fflag_view.append_column(column_value)
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_child(self.fflag_view)
        scrolled.set_vexpand(True)
        fflags_box.append(scrolled)
        self.fflags_text = Gtk.TextView()
        self.fflags_text.set_editable(False)
        self.fflags_text.set_vexpand(False)
        fflags_box.append(self.fflags_text)
        self.stack.add_titled(fflags_box, "fflags", "FFlags")
        credits_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16, margin_top=40, margin_bottom=40, margin_start=40, margin_end=40)
        credits_title = Gtk.Label(label="Credits")
        credits_title.set_margin_bottom(10)
        credits_title.set_markup("<span size='xx-large' weight='bold'>Credits</span>")
        credits_box.append(credits_title)
        author_label = Gtk.Label(label="Developed by: Nhet_444")
        author_label.set_margin_bottom(8)
        author_label.set_markup("<b>Developed by:</b> Nhet_444")
        credits_box.append(author_label)
        yt_label = Gtk.Label()
        yt_label.set_markup("<a href='https://www.youtube.com/@Nhet_444'>YouTube: @Nhet_444</a>")
        yt_label.set_selectable(True)
        yt_label.set_margin_bottom(8)
        credits_box.append(yt_label)
        thanks_label = Gtk.Label(label="Thank you for using Lukus!\nIf you like this project, consider subscribing and supporting on YouTube.")
        thanks_label.set_justify(Gtk.Justification.CENTER)
        credits_box.append(thanks_label)
        self.stack.add_titled(credits_box, "creditos", "Credits")
        self.load_fflags()
        self.apply_dark_mode()
    def set_easy_fflag(self, name, value):
        found = False
        for row in self.fflag_store:
            if row[0] == name:
                row[1] = value
                found = True
                break
        if not found:
            self.fflag_store.append([name, value])
        self.update_fflags_text()
    def update_fflags_text(self):
        buf = self.fflags_text.get_buffer()
        fflags = {}
        for row in self.fflag_store:
            fflags[row[0]] = self.parse_value(row[1])
        buf.set_text(json.dumps(fflags, indent=4, ensure_ascii=False))
    def parse_value(self, value):
        v = value.strip()
        if v.lower() == 'true':
            return True
        if v.lower() == 'false':
            return False
        try:
            if '.' in v:
                return float(v)
            return int(v)
        except ValueError:
            return v
    def load_fflags(self):
        for row in list(self.fflag_store):
            self.fflag_store.remove(row.iter)
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    data = json.load(f)
                fflags = data.get("fflags", {})
                for key, value in fflags.items():
                    self.fflag_store.append([key, str(value)])
                # Set switches based on loaded FFlags
                if str(fflags.get("DFFlagDebugRenderForceTechnologyVoxel", "")).lower() == "true":
                    self.switch_voxel.set_active(True)
                else:
                    self.switch_voxel.set_active(False)
                if str(fflags.get("FFlagDebugForceFutureIsBrightPhase2", "")).lower() == "true":
                    self.switch_shadow.set_active(True)
                else:
                    self.switch_shadow.set_active(False)
                if str(fflags.get("FFlagDebugForceFutureIsBrightPhase3", "")).lower() == "true":
                    self.switch_future.set_active(True)
                else:
                    self.switch_future.set_active(False)
            except Exception as e:
                print(f"Error reading config.json: {e}")
    def on_add_fflag(self, button):
        fflag = self.fflag_entry.get_text().strip()
        value = self.value_entry.get_text().strip()
        if fflag and value:
            self.fflag_store.append([fflag, value])
            self.fflag_entry.set_text("")
            self.value_entry.set_text("")
            self.update_fflags_text()
    def on_remove_fflag(self, button):
        # Gtk4: Use GtkSingleSelection for selection
        selection = self.fflag_view.get_selection() if hasattr(self.fflag_view, 'get_selection') else None
        if selection:
            model, treeiter = selection.get_selected()
            if treeiter:
                model.remove(treeiter)
                self.update_fflags_text()
        else:
            # Fallback: remove first selected row (Gtk4+)
            selected_rows = self.fflag_view.get_selection().get_selected_rows() if hasattr(self.fflag_view.get_selection(), 'get_selected_rows') else []
            for path in selected_rows:
                self.fflag_store.remove(self.fflag_store.get_iter(path))
            self.update_fflags_text()
    def on_fflag_edited(self, widget, path, text, column):
        self.fflag_store[path][column] = text
        self.update_fflags_text()

    def on_clear_fflags(self, button):
        for row in list(self.fflag_store):
            self.fflag_store.remove(row.iter)
        self.update_fflags_text()
    def on_save_fflags(self, button):
        if os.path.exists(self.config_path):
            import shutil
            backup_path = self.config_path + ".bak"
            shutil.copy2(self.config_path, backup_path)
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    data = json.load(f)
                fflags = {}
                for row in self.fflag_store:
                    fflags[row[0]] = self.parse_value(row[1])
                data["fflags"] = fflags
                with open(self.config_path, "w") as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                self.show_info("FFlags saved successfully! (Backup created)")
                self.update_fflags_text()
            except Exception as e:
                self.show_error(f"Error saving config.json: {e}")
        else:
            self.show_error("config.json file not found!")
    def on_import_fflags(self, button):
        dialog = Gtk.FileChooserDialog(
            title="Select FFlags JSON File",
            transient_for=self,
            modal=True,
            action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("Open", Gtk.ResponseType.OK)
        filter_json = Gtk.FileFilter()
        filter_json.set_name("JSON files")
        filter_json.add_pattern("*.json")
        dialog.add_filter(filter_json)

        def on_response(dlg, response_id):
            if response_id == Gtk.ResponseType.OK:
                file = dlg.get_file()
                if file:
                    filename = file.get_path()
                    try:
                        with open(filename, "r") as f:
                            data = json.load(f)
                        fflags = data.get("fflags", data)
                        for row in list(self.fflag_store):
                            self.fflag_store.remove(row.iter)
                        for key, value in fflags.items():
                            self.fflag_store.append([key, str(value)])
                        self.update_fflags_text()
                        self.show_info("FFlags imported successfully!")
                    except Exception as e:
                        self.show_error(f"Failed to import FFlags: {e}")
            dlg.destroy()

        dialog.connect("response", on_response)
        dialog.present()

    def apply_dark_mode(self):
        settings = Gtk.Settings.get_default()
        if settings:
            settings.set_property("gtk-application-prefer-dark-theme", True)
    def show_error(self, message):
        dialog = Gtk.MessageDialog(transient_for=self, modal=True, buttons=Gtk.ButtonsType.CLOSE, message_type=Gtk.MessageType.ERROR, text=message)
        dialog.connect("response", lambda d, r: d.destroy())
        dialog.present()
    def show_info(self, message):
        dialog = Gtk.MessageDialog(transient_for=self, modal=True, buttons=Gtk.ButtonsType.CLOSE, message_type=Gtk.MessageType.INFO, text=message)
        dialog.connect("response", lambda d, r: d.destroy())
        dialog.present()
    def on_apply_easy(self, button):
        fps = self.fps_entry.get_text().strip()
        if fps:
            self.set_easy_fflag("DFIntTaskSchedulerTargetFps", fps)
        if self.fflag_occlusion.get_active():
            self.set_easy_fflag("DFFlagUseVisBugChecks", "True")
        else:
            self.remove_easy_fflag("DFFlagUseVisBugChecks")
        if self.switch_voxel.get_active():
            self.set_easy_fflag("DFFlagDebugRenderForceTechnologyVoxel", "True")
        else:
            self.remove_easy_fflag("DFFlagDebugRenderForceTechnologyVoxel")
        if self.switch_shadow.get_active():
            self.set_easy_fflag("FFlagDebugForceFutureIsBrightPhase2", "True")
        else:
            self.remove_easy_fflag("FFlagDebugForceFutureIsBrightPhase2")
        if self.switch_future.get_active():
            self.set_easy_fflag("FFlagDebugForceFutureIsBrightPhase3", "True")
        else:
            self.remove_easy_fflag("FFlagDebugForceFutureIsBrightPhase3")
        if self.switch_avatar_chat.get_active():
            self.set_easy_fflag("FFlagDebugAvatarChatVisualization", "True")
        else:
            self.remove_easy_fflag("FFlagDebugAvatarChatVisualization")
        if self.switch_hyper.get_active():
            self.set_easy_fflag("FFlagDebugCheckRenderThreading", "True")
            self.set_easy_fflag("FFlagRenderDebugCheckThreading2", "True")
        else:
            self.remove_easy_fflag("FFlagDebugCheckRenderThreading")
            self.remove_easy_fflag("FFlagRenderDebugCheckThreading2")
        if self.spin_max_threads.get_value() != 2400:
            self.set_easy_fflag("FIntRuntimeMaxNumOfThreads", str(int(self.spin_max_threads.get_value())))
        else:
            self.remove_easy_fflag("FIntRuntimeMaxNumOfThreads")
        if self.spin_min_threads.get_value() != 3:
            self.set_easy_fflag("FIntTaskSchedulerThreadMin", str(int(self.spin_min_threads.get_value())))
        else:
            self.remove_easy_fflag("FIntTaskSchedulerThreadMin")
        if self.switch_smooth_terrain.get_active():
            self.set_easy_fflag("FFlagDebugRenderingSetDeterministic", "True")
        else:
            self.remove_easy_fflag("FFlagDebugRenderingSetDeterministic")
        if self.switch_quality.get_active():
            self.set_easy_fflag("FIntRomarkStartWithGraphicQualityLevel", str(int(self.spin_quality.get_value())))
        else:
            self.remove_easy_fflag("FIntRomarkStartWithGraphicQualityLevel")
        if self.switch_terrain.get_active():
            self.set_easy_fflag("FIntTerrainArraySliceSize", str(int(self.spin_terrain.get_value())))
        else:
            self.remove_easy_fflag("FIntTerrainArraySliceSize")
        if self.switch_no_shadows.get_active():
            self.set_easy_fflag("FIntRenderShadowIntensity", "0")
        else:
            self.remove_easy_fflag("FIntRenderShadowIntensity")
        if self.switch_dpi.get_active():
            self.set_easy_fflag("DFFlagDisableDPIScale", "True")
        else:
            self.remove_easy_fflag("DFFlagDisableDPIScale")
        if self.switch_wind.get_active():
            self.set_easy_fflag("FFlagGlobalWindRendering", "True")
            self.set_easy_fflag("FFlagGlobalWindActivated", "True")
        else:
            self.remove_easy_fflag("FFlagGlobalWindRendering")
            self.remove_easy_fflag("FFlagGlobalWindActivated")
        if self.switch_postfx.get_active():
            self.set_easy_fflag("FFlagDisablePostFx", "True")
        else:
            self.remove_easy_fflag("FFlagDisablePostFx")
        if self.switch_gray_sky.get_active():
            self.set_easy_fflag("FFlagDebugSkyGray", "True")
        else:
            self.remove_easy_fflag("FFlagDebugSkyGray")
        if self.switch_light_atten.get_active():
            self.set_easy_fflag("FFlagNewLightAttenuation", "True")
        else:
            self.remove_easy_fflag("FFlagNewLightAttenuation")
        if self.switch_gpu_culling.get_active():
            self.set_easy_fflag("FFlagFastGPULightCulling3", "True")
        else:
            self.remove_easy_fflag("FFlagFastGPULightCulling3")
        if self.switch_high_tex.get_active():
            self.set_easy_fflag("DFFlagTextureQualityOverrideEnabled", "True")
        else:
            self.remove_easy_fflag("DFFlagTextureQualityOverrideEnabled")
        if self.switch_quality.get_active():
            self.set_easy_fflag("DFIntTextureQualityOverride", str(int(self.spin_quality.get_value())))
        else:
            self.remove_easy_fflag("DFIntTextureQualityOverride")
        if self.spin_low_tex.get_value() != -1:
            self.set_easy_fflag("DFIntPerformanceControlTextureQualityBestUtility", str(int(self.spin_low_tex.get_value())))
        else:
            self.remove_easy_fflag("DFIntPerformanceControlTextureQualityBestUtility")
        if self.switch_no_avatar_tex.get_active():
            self.set_easy_fflag("DFIntTextureCompositorActiveJobs", "0")
        else:
            self.remove_easy_fflag("DFIntTextureCompositorActiveJobs")
        if self.switch_no_grass.get_active():
            self.set_easy_fflag("FIntFRMMinGrassDistance", "0")
            self.set_easy_fflag("FIntFRMMaxGrassDistance", "0")
            self.set_easy_fflag("FIntRenderGrassDetailStrands", "0")
            self.set_easy_fflag("FIntRenderGrassHeightScaler", "0")
        else:
            self.remove_easy_fflag("FIntFRMMinGrassDistance")
            self.remove_easy_fflag("FIntFRMMaxGrassDistance")
            self.remove_easy_fflag("FIntRenderGrassDetailStrands")
            self.remove_easy_fflag("FIntRenderGrassHeightScaler")
        if self.switch_fb.get_active():
            self.set_easy_fflag("DFIntMaxFrameBufferSize", str(int(self.spin_fb.get_value())))
        else:
            self.remove_easy_fflag("DFIntMaxFrameBufferSize")
        if self.switch_msaa.get_active():
            self.set_easy_fflag("FIntDebugForceMSAASamples", str(int(self.spin_msaa.get_value())))
        else:
            self.remove_easy_fflag("FIntDebugForceMSAASamples")
        if self.switch_bias.get_active():
            self.set_easy_fflag("FIntRenderShadowmapBias", str(int(self.spin_bias.get_value())))
        else:
            self.remove_easy_fflag("FIntRenderShadowmapBias")
        if self.switch_outline.get_active():
            self.set_easy_fflag("DFFlagDebugDrawBroadPhaseAABBs", "True")
        else:
            self.remove_easy_fflag("DFFlagDebugDrawBroadPhaseAABBs")
        if self.switch_xray.get_active():
            self.set_easy_fflag("FIntCameraFarZPlane", "1")
        else:
            self.remove_easy_fflag("FIntCameraFarZPlane")
        self.show_info("Configurações aplicadas ao campo de FFlags!")
    def remove_easy_fflag(self, name):
        for row in self.fflag_store:
            if row[0] == name:
                self.fflag_store.remove(row.iter)
                break
        self.update_fflags_text()
class LukuApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.luku.sober")
    def do_activate(self):
        win = LukuWindow(self)
        win.present()
if __name__ == "__main__":
    app = LukuApp()
    app.run()
