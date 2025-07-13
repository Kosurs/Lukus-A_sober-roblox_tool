import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
import os
import json
import urllib.request
from gi.repository import Gtk, GLib, GdkPixbuf, Gdk, GObject, Gio

class FFlagItem(GObject.Object):
    __gtype_name__ = 'FFlagItem'
    name = GObject.Property(type=str)
    value = GObject.Property(type=str)
    def __init__(self, name, value):
        super().__init__()
        self.name = name
        self.value = value

class LukuWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.set_title("Lukus - Sober FFlags Modifier")
        self.set_default_size(700, 450)
        settings = Gtk.Settings.get_default()
        settings.set_property("gtk-application-prefer-dark-theme", True)
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.set_child(main_box)
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12,
                           margin_start=10, margin_end=10, margin_top=10, margin_bottom=10)
        header_box.add_css_class("header")
        self.logo_path = self.download_logo(
            "https://i.postimg.cc/KYg2SKGf/59a711a4-5083-43ac-a1fd-216876fba3e2-removalai-preview.png",
            "/tmp/lukus_logo.png"
        )
        if self.logo_path:
            try:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    self.logo_path, 64, 64, True
                )
                logo_picture = Gtk.Picture()
                logo_picture.set_pixbuf(pixbuf)
                logo_picture.set_content_fit(Gtk.ContentFit.CONTAIN)
                header_box.append(logo_picture)
            except Exception as e:
                print(f"Error loading logo: {e}")
        title_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, valign=Gtk.Align.CENTER)
        app_title = Gtk.Label(label="Lukus - Sober FFlags Modifier")
        app_title.add_css_class("app-title")
        app_title.set_xalign(0)
        title_box.append(app_title)
        subtitle = Gtk.Label(label="Optimize your Roblox experience")
        subtitle.add_css_class("app-subtitle")
        subtitle.set_xalign(0)
        title_box.append(subtitle)
        header_box.append(title_box)
        main_box.append(header_box)
        separator = Gtk.Separator()
        main_box.append(separator)
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(300)
        switcher = Gtk.StackSwitcher(stack=self.stack)
        switcher.set_margin_top(10)
        switcher.set_margin_bottom(10)
        main_box.append(switcher)
        main_box.append(self.stack)
        self.config_path = os.path.expanduser("~/.var/app/org.vinegarhq.Sober/config/sober/config.json")
        self.sober_dir = os.path.dirname(self.config_path)
        if not self.check_sober_installation():
            self.show_error("Sober folder not found!\nPlease install and run Sober at least once.")
            return
        self.create_easy_access_page()
        self.create_fflags_page()
        self.create_credits_page()
        self.load_fflags()

    def download_logo(self, url, path):
        try:
            if not os.path.exists(path):
                urllib.request.urlretrieve(url, path)
            return path
        except Exception as e:
            print(f"Error downloading logo: {e}")
            return None

    def check_sober_installation(self):
        # Verifica se o Sober está instalado
        flatpak_path = os.path.expanduser("~/.var/app/org.vinegarhq.Sober")
        return os.path.exists(flatpak_path)

    def create_frame(self, title, orientation=Gtk.Orientation.VERTICAL):
        frame = Gtk.Frame(label=title)
        box = Gtk.Box(orientation=orientation, spacing=12, 
                      margin_top=12, margin_bottom=12, 
                      margin_start=12, margin_end=12)
        frame.set_child(box)
        return frame, box

    def create_switch_row(self, container, label, active=False, tooltip=None):
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        row.append(Gtk.Label(label=label, hexpand=True, xalign=0))
        switch = Gtk.Switch(active=active)
        if tooltip:
            switch.set_tooltip_text(tooltip)
        row.append(switch)
        container.append(row)
        return switch

    def create_spin_row(self, container, label, min_val, max_val, step, value, tooltip=None):
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        row.append(Gtk.Label(label=label, hexpand=True, xalign=0))
        spin = Gtk.SpinButton()
        spin.set_range(min_val, max_val)
        spin.set_increments(step, step * 5)
        spin.set_value(value)
        if tooltip:
            spin.set_tooltip_text(tooltip)
        row.append(spin)
        container.append(row)
        return spin

    def create_switch_spin_row(self, container, label, min_val, max_val, step, value, active=False, tooltip=None):
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        row.append(Gtk.Label(label=label, hexpand=True, xalign=0))
        
        switch = Gtk.Switch(active=active)
        row.append(switch)
        
        spin = Gtk.SpinButton()
        spin.set_range(min_val, max_val)
        spin.set_increments(step, step * 5)
        spin.set_value(value)
        spin.set_sensitive(active)
        
        # Conectar switch para habilitar/desabilitar spin
        switch.connect("state-set", lambda s, state: spin.set_sensitive(state))
        
        if tooltip:
            switch.set_tooltip_text(tooltip)
            spin.set_tooltip_text(tooltip)
        
        row.append(spin)
        container.append(row)
        return switch, spin

    def create_easy_access_page(self):
        # Container principal com scroll
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        
        # Box principal
        easy_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, 
                          spacing=24, 
                          margin_top=10, margin_bottom=10,
                          margin_start=20, margin_end=20)
        
        # Título
        title = Gtk.Label(label="Easy Configuration")
        title.add_css_class("section-title")
        easy_box.append(title)
        
        # FPS Unlock
        fps_frame, fps_box = self.create_frame("FPS Unlock")
        self.fps_entry = self.create_spin_row(
            fps_box, "FPS:", 1, 1000, 5, 60,
            "Set your desired FPS limit (60 is recommended for most systems)"
        )
        easy_box.append(fps_frame)
        
        # Occlusion Culling
        occ_frame, occ_box = self.create_frame("Occlusion Culling")
        self.fflag_occlusion = self.create_switch_row(
            occ_box, "Enable", False,
            "Improves performance by not rendering objects that are not visible"
        )
        easy_box.append(occ_frame)
        
        # Lighting Technologies
        lighting_frame, lighting_box = self.create_frame("Lightning Technologies")
        self.switch_voxel = self.create_switch_row(
            lighting_box, "Voxel Lighting (Phase 1)", False,
            "Experimental voxel-based lighting system"
        )
        self.switch_shadow = self.create_switch_row(
            lighting_box, "Shadowmap Lighting (Phase 2)", False,
            "Improved shadow rendering technology"
        )
        self.switch_future = self.create_switch_row(
            lighting_box, "Future Lighting (Phase 3)", False,
            "Next-generation lighting system (may impact performance)"
        )
        easy_box.append(lighting_frame)
        
        # Advanced Graphics
        advanced_frame, advanced_box = self.create_frame("Advanced Graphics")
        
        self.switch_avatar_chat = self.create_switch_row(
            advanced_box, "Avatar Chat Visualization", False,
            "Visual indicators for avatar chat"
        )
        # Switch para ativar configurações de threads
        self.switch_threads = self.create_switch_row(
            advanced_box, "Ativar configurações de threads", False,
            "Habilita opções de HyperThreading e número de threads"
        )
        self.switch_hyper = self.create_switch_row(
            advanced_box, "HyperThreading", False,
            "Utilize CPU hyperthreading capabilities"
        )
        self.spin_max_threads = self.create_spin_row(
            advanced_box, "Maximum Threads:", 1, 128, 1, 0,
            "Maximum CPU threads to use (set to 0 for auto-detect)"
        )
        self.spin_min_threads = self.create_spin_row(
            advanced_box, "Minimum Threads:", 1, 16, 1, 0,
            "Minimum CPU threads to reserve"
        )
        # Habilitar/desabilitar controles de threads conforme switch
        self.switch_threads.connect("state-set", lambda s, state: [self.switch_hyper.set_sensitive(state), self.spin_max_threads.set_sensitive(state), self.spin_min_threads.set_sensitive(state)])
        self.switch_hyper.set_sensitive(False)
        self.spin_max_threads.set_sensitive(False)
        self.spin_min_threads.set_sensitive(False)
        self.switch_smooth_terrain = self.create_switch_row(
            advanced_box, "Smoother Terrain", False,
            "Improve terrain rendering quality"
        )
        
        # Graphics Quality
        self.switch_quality, self.spin_quality = self.create_switch_spin_row(
            advanced_box, "Graphics Quality Level:", 1, 10, 1, 1, False,
            "Higher values = better graphics but lower performance"
        )

        # Terrain Textures
        self.switch_terrain, self.spin_terrain = self.create_switch_spin_row(
            advanced_box, "Low Quality Terrain Textures:", 4, 64, 4, 4, False,
            "Lower values reduce texture quality to improve performance"
        )
        
        # Outras opções
        self.switch_no_shadows = self.create_switch_row(
            advanced_box, "Disable Shadows", False,
            "Disable shadows for better performance"
        )
        self.switch_dpi = self.create_switch_row(
            advanced_box, "Preserve rendering quality with display setting", False,
            "Maintain consistent quality across different DPI settings"
        )
        self.switch_wind = self.create_switch_row(
            advanced_box, "Disable Wind", False,
            "Disable wind effects for better performance"
        )
        self.switch_postfx = self.create_switch_row(
            advanced_box, "Disable PostFX", False,
            "Disable post-processing effects"
        )
        self.switch_gray_sky = self.create_switch_row(
            advanced_box, "Gray Sky", False,
            "Use simplified sky rendering"
        )
        self.switch_light_atten = self.create_switch_row(
            advanced_box, "Lighting Attenuation", False,
            "Control how light diminishes over distance"
        )
        self.switch_gpu_culling = self.create_switch_row(
            advanced_box, "Enable GPULightCulling", False,
            "Use GPU for light culling (requires compatible hardware)"
        )
        
        # Frame Buffer
        self.switch_fb, self.spin_fb = self.create_switch_spin_row(
            advanced_box, "Frame Buffer:", 0, 10, 1, 0, False,
            "Frame buffer size (higher = better quality but more VRAM usage)"
        )
        
        # Textures
        self.switch_high_tex = self.create_switch_row(
            advanced_box, "High Quality Textures", False,
            "Enable higher resolution textures"
        )
        self.spin_low_tex = self.create_spin_row(
            advanced_box, "Lower Quality Textures:", -1, 3, 1, -1,
            "Set to -1 for automatic quality based on hardware"
        )
        self.switch_no_avatar_tex = self.create_switch_row(
            advanced_box, "No avatar textures", False,
            "Disable avatar textures to reduce VRAM usage"
        )
        self.switch_no_grass = self.create_switch_row(
            advanced_box, "Remove Grass", False,
            "Disable grass rendering for better performance"
        )
        
        # MSAA
        self.switch_msaa, self.spin_msaa = self.create_switch_spin_row(
            advanced_box, "Force MSAA:", 0, 16, 2, 0, False,
            "Multisample anti-aliasing (higher = smoother edges but more GPU load)"
        )

        # ShadowMap
        self.switch_bias, self.spin_bias = self.create_switch_spin_row(
            advanced_box, "ShadowMap Bias:", 0, 100, 1, 0, False,
            "Adjust shadow rendering accuracy"
        )
        
        # Outros efeitos
        self.switch_outline = self.create_switch_row(
            advanced_box, "Humanoid Outline", False,
            "Enable character outlines"
        )
        self.switch_xray = self.create_switch_row(
            advanced_box, "Buggy ZPlane Camera (Xray)", False,
            "Experimental camera mode (may cause visual glitches)"
        )
        
        easy_box.append(advanced_frame)
        
        # Botão aplicar
        apply_btn = Gtk.Button(label="Apply Settings", margin_top=20)
        apply_btn.add_css_class("suggested-action")
        apply_btn.connect("clicked", self.on_apply_easy)
        easy_box.append(apply_btn)
        
        scroll.set_child(easy_box)
        self.stack.add_titled(scroll, "easy", "Easy Access")

    def create_fflags_page(self):
        fflags_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, 
                            spacing=12, 
                            margin_top=12, margin_bottom=12,
                            margin_start=12, margin_end=12)
        
        # Título
        title = Gtk.Label(label="Advanced FFlags Editor")
        title.add_css_class("section-title")
        fflags_box.append(title)
        
        # Caminho do arquivo
        path_label = Gtk.Label(label=f"Config: {self.config_path}")
        path_label.set_xalign(0)
        path_label.set_selectable(True)
        path_label.set_margin_bottom(10)
        fflags_box.append(path_label)
        
        # Entrada de FFlags
        entry_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.fflag_entry = Gtk.Entry(placeholder_text="FFlag name", hexpand=True)
        self.value_entry = Gtk.Entry(placeholder_text="Value (true/false/number)")
        entry_box.append(self.fflag_entry)
        entry_box.append(self.value_entry)
        fflags_box.append(entry_box)
        
        # Botões
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        add_button = Gtk.Button(label="Add FFlag", tooltip_text="Add a new FFlag")
        add_button.connect("clicked", self.on_add_fflag)
        remove_button = Gtk.Button(label="Remove Selected", tooltip_text="Remove selected FFlag")
        remove_button.connect("clicked", self.on_remove_fflag)
        save_button = Gtk.Button(label="Save FFlags", tooltip_text="Save changes to config file")
        save_button.connect("clicked", self.on_save_fflags)
        save_button.add_css_class("suggested-action")
        import_button = Gtk.Button(label="Import", tooltip_text="Import FFlags from JSON file")
        import_button.connect("clicked", self.on_import_fflags)
        clear_button = Gtk.Button(label="Delete All Flags", tooltip_text="Remove all FFlags")
        clear_button.connect("clicked", self.on_clear_fflags)
        
        button_box.append(add_button)
        button_box.append(remove_button)
        button_box.append(save_button)
        button_box.append(import_button)
        button_box.append(clear_button)
        fflags_box.append(button_box)
        
        # Lista de FFlags usando Gio.ListStore
        self.fflag_store = Gio.ListStore(item_type=FFlagItem)
        
        # Usar ColumnView com SingleSelection
        self.selection = Gtk.SingleSelection(model=self.fflag_store)
        self.fflag_view = Gtk.ColumnView(model=self.selection)
        
        # Coluna FFlag
        fflag_factory = Gtk.SignalListItemFactory()
        fflag_factory.connect("setup", self.on_fflag_factory_setup)
        fflag_factory.connect("bind", self.on_fflag_factory_bind)
        
        fflag_column = Gtk.ColumnViewColumn(title="FFlag", factory=fflag_factory)
        self.fflag_view.append_column(fflag_column)
        
        # Coluna Valor
        value_factory = Gtk.SignalListItemFactory()
        value_factory.connect("setup", self.on_value_factory_setup)
        value_factory.connect("bind", self.on_value_factory_bind)
        
        value_column = Gtk.ColumnViewColumn(title="Value", factory=value_factory)
        self.fflag_view.append_column(value_column)
        
        # Scrolled Window
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_child(self.fflag_view)
        scrolled.set_vexpand(True)
        fflags_box.append(scrolled)
        
        # Visualização JSON com scroller e altura fixa
        json_frame = Gtk.Frame(label="JSON Preview", margin_top=10)
        scrolled_json = Gtk.ScrolledWindow()
        scrolled_json.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_json.set_min_content_height(150)
        scrolled_json.set_max_content_height(200)
        self.fflags_text = Gtk.TextView()
        self.fflags_text.set_editable(False)
        self.fflags_text.set_monospace(True)
        scrolled_json.set_child(self.fflags_text)
        json_frame.set_child(scrolled_json)
        fflags_box.append(json_frame)
        
        self.stack.add_titled(fflags_box, "fflags", "Advanced FFlags")

    def on_fflag_factory_setup(self, factory, list_item):
        label = Gtk.Label()
        label.set_xalign(0)
        list_item.set_child(label)

    def on_fflag_factory_bind(self, factory, list_item):
        label = list_item.get_child()
        item = list_item.get_item()
        if item:
            label.set_text(item.name)

    def on_value_factory_setup(self, factory, list_item):
        entry = Gtk.Entry()
        entry.set_hexpand(True)
        list_item.set_child(entry)

    def on_value_factory_bind(self, factory, list_item):
        entry = list_item.get_child()
        item = list_item.get_item()
        if item:
            entry.set_text(item.value)
            entry.connect("changed", self.on_value_changed, item)

    def on_value_changed(self, entry, item):
        new_value = entry.get_text()
        item.value = new_value
        self.update_fflags_text()

    def create_credits_page(self):
        credits_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, 
                             spacing=16, 
                             margin_top=40, margin_bottom=40,
                             margin_start=40, margin_end=40)
        
        credits_title = Gtk.Label(label="Credits")
        credits_title.add_css_class("section-title")
        credits_box.append(credits_title)
        
        author_label = Gtk.Label(label="Developed by: Nhet_444")
        author_label.set_markup("<b>Developed by:</b> Nhet_444")
        author_label.set_margin_bottom(8)
        credits_box.append(author_label)
        
        yt_label = Gtk.Label()
        yt_label.set_markup("<a href='https://www.youtube.com/@Nhet_444'>YouTube: @Nhet_444</a>")
        yt_label.set_selectable(True)
        yt_label.set_margin_bottom(8)
        credits_box.append(yt_label)
        
        github_label = Gtk.Label()
        github_label.set_markup("<a href='https://github.com/Kosurs/Lukus-A_sober-roblox_tool'>GitHub Repository</a>")
        github_label.set_selectable(True)
        github_label.set_margin_bottom(20)
        credits_box.append(github_label)
        
        thanks_label = Gtk.Label(label="Thank you for using Lukus!\n\n"
                                     "If you like this project, consider supporting on YouTube.\n\n"
                                     "Report issues or contribute on GitHub!")
        thanks_label.set_justify(Gtk.Justification.CENTER)
        credits_box.append(thanks_label)
        
        self.stack.add_titled(credits_box, "creditos", "Credits")

    def set_easy_fflag(self, name, value):
        # Verificar se já existe
        for i in range(self.fflag_store.get_n_items()):
            item = self.fflag_store.get_item(i)
            if item.name == name:
                item.value = str(value)
                return
        # Se não existe, adicionar novo
        self.fflag_store.append(FFlagItem(name, str(value)))
        self.update_fflags_text()

    def remove_easy_fflag(self, name):
        for i in range(self.fflag_store.get_n_items()):
            item = self.fflag_store.get_item(i)
            if item.name == name:
                self.fflag_store.remove(i)
                break
        self.update_fflags_text()

    def parse_value(self, value_str):
        value_str = value_str.strip()
        if value_str.lower() == 'true':
            return True
        if value_str.lower() == 'false':
            return False
        
        # Tentar converter para número
        try:
            # Primeiro tenta como int
            return int(value_str)
        except ValueError:
            try:
                f_val = float(value_str)
                # Se for inteiro, retorna int
                if f_val.is_integer():
                    return int(f_val)
                return f_val
            except ValueError:
                return value_str

    def update_fflags_text(self):
        buf = self.fflags_text.get_buffer()
        fflags = {}
        for i in range(self.fflag_store.get_n_items()):
            item = self.fflag_store.get_item(i)
            fflags[item.name] = self.parse_value(item.value)
        buf.set_text(json.dumps(fflags, indent=4, ensure_ascii=False))

    def load_fflags(self):
        if not os.path.exists(self.config_path):
            self.show_warning("Config file not found. Creating new one on save.")
            return
            
        try:
            with open(self.config_path, "r") as f:
                data = json.load(f)
                
            fflags = data.get("fflags", {})
            self.fflag_store.remove_all()
            
            for key, value in fflags.items():
                self.fflag_store.append(FFlagItem(key, str(value)))

            # Não atualizar UI do Easy Access com os valores carregados
            # Apenas atualizar o preview JSON
            self.update_fflags_text()
            
        except Exception as e:
            self.show_error(f"Error reading config.json: {str(e)}")

    def update_easy_ui_from_fflags(self, fflags):
        # Função auxiliar para obter valores com fallback
        def get_value(key, default, type_cast=str):
            value = fflags.get(key, default)
            try:
                return type_cast(value)
            except:
                return default
                
        # Atualizar controles da UI
        self.fps_entry.set_value(get_value("DFIntTaskSchedulerTargetFps", 60, int))
        self.fflag_occlusion.set_active(get_value("DFFlagUseVisBugChecks", False, bool))
        self.switch_voxel.set_active(get_value("DFFlagDebugRenderForceTechnologyVoxel", False, bool))
        self.switch_shadow.set_active(get_value("FFlagDebugForceFutureIsBrightPhase2", False, bool))
        self.switch_future.set_active(get_value("FFlagDebugForceFutureIsBrightPhase3", False, bool))
        self.switch_avatar_chat.set_active(get_value("FFlagDebugAvatarChatVisualization", False, bool))
        self.switch_hyper.set_active(get_value("FFlagDebugCheckRenderThreading", False, bool))
        self.spin_max_threads.set_value(get_value("FIntRuntimeMaxNumOfThreads", 4, int))
        self.spin_min_threads.set_value(get_value("FIntTaskSchedulerThreadMin", 2, int))
        self.switch_smooth_terrain.set_active(get_value("FFlagDebugRenderingSetDeterministic", False, bool))
        
        # Graphics Quality
        quality_active = "FIntRomarkStartWithGraphicQualityLevel" in fflags
        self.switch_quality.set_active(quality_active)
        if quality_active:
            self.spin_quality.set_value(get_value("FIntRomarkStartWithGraphicQualityLevel", 5, int))
        
        # Terrain Textures
        terrain_active = "FIntTerrainArraySliceSize" in fflags
        self.switch_terrain.set_active(terrain_active)
        if terrain_active:
            self.spin_terrain.set_value(get_value("FIntTerrainArraySliceSize", 16, int))
        
        # Outras opções
        self.switch_no_shadows.set_active(get_value("FIntRenderShadowIntensity", 0, int) == 0)
        self.switch_dpi.set_active(get_value("DFFlagDisableDPIScale", False, bool))
        self.switch_wind.set_active(get_value("FFlagGlobalWindRendering", True, bool))
        self.switch_postfx.set_active(get_value("FFlagDisablePostFx", False, bool))
        self.switch_gray_sky.set_active(get_value("FFlagDebugSkyGray", False, bool))
        self.switch_light_atten.set_active(get_value("FFlagNewLightAttenuation", False, bool))
        self.switch_gpu_culling.set_active(get_value("FFlagFastGPULightCulling3", False, bool))
        self.switch_high_tex.set_active(get_value("DFFlagTextureQualityOverrideEnabled", False, bool))
        self.spin_low_tex.set_value(get_value("DFIntPerformanceControlTextureQualityBestUtility", -1, int))
        self.switch_no_avatar_tex.set_active(get_value("DFIntTextureCompositorActiveJobs", 0, int) == 0)
        self.switch_no_grass.set_active(get_value("FIntFRMMinGrassDistance", 0, int) == 0)
        
        # Frame Buffer
        fb_active = "DFIntMaxFrameBufferSize" in fflags
        self.switch_fb.set_active(fb_active)
        if fb_active:
            self.spin_fb.set_value(get_value("DFIntMaxFrameBufferSize", 4, int))
        
        # MSAA
        msaa_active = "FIntDebugForceMSAASamples" in fflags
        self.switch_msaa.set_active(msaa_active)
        if msaa_active:
            self.spin_msaa.set_value(get_value("FIntDebugForceMSAASamples", 4, int))
        
        # ShadowMap
        bias_active = "FIntRenderShadowmapBias" in fflags
        self.switch_bias.set_active(bias_active)
        if bias_active:
            self.spin_bias.set_value(get_value("FIntRenderShadowmapBias", 75, int))
        
        self.switch_outline.set_active(get_value("DFFlagDebugDrawBroadPhaseAABBs", False, bool))
        self.switch_xray.set_active(get_value("FIntCameraFarZPlane", 1, int) == 1)

    def on_add_fflag(self, button):
        fflag = self.fflag_entry.get_text().strip()
        value = self.value_entry.get_text().strip()
        fixed = False

        # Corrigir vírgula no final do nome
        if fflag.endswith(","):
            fflag = fflag.rstrip(",").strip()
            fixed = True

        # Corrigir vírgula no final do valor
        if value.endswith(","):
            value = value.rstrip(",").strip()
            fixed = True

        if not fflag:
            self.show_error("FFlag name cannot be empty!")
            return

        if not value:
            self.show_error("Value cannot be empty!")
            return

        # Verificar se já existe
        for i in range(self.fflag_store.get_n_items()):
            item = self.fflag_store.get_item(i)
            if item.name == fflag:
                self.show_error(f"FFlag '{fflag}' already exists!")
                return

        self.fflag_store.append(FFlagItem(fflag, value))
        self.fflag_entry.set_text("")
        self.value_entry.set_text("")
        self.update_fflags_text()
        if fixed:
            self.show_info("Trailing comma detected and fixed automatically!")
        else:
            self.show_info(f"FFlag '{fflag}' added successfully!")

    def on_remove_fflag(self, button):
        position = self.selection.get_selected()
        if position != Gtk.INVALID_LIST_POSITION:
            item = self.fflag_store.get_item(position)
            self.fflag_store.remove(position)
            self.update_fflags_text()
            self.show_info(f"FFlag '{item.name}' removed!")

    def on_clear_fflags(self, button):
        if self.fflag_store.get_n_items() == 0:
            return
            
        dialog = Gtk.MessageDialog(
            transient_for=self,
            modal=True,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text="Delete All Flags?",
    secondary_text="This will permanently remove all FFlags. Are you sure?"
)
        
        def on_response(dialog, response):
            if response == Gtk.ResponseType.YES:
                self.fflag_store.remove_all()
                self.update_fflags_text()
                self.show_info("All FFlags deleted!")
            dialog.destroy()
        
        dialog.connect("response", on_response)
        dialog.present()

    def on_save_fflags(self, button):
        # Criar diretório se não existir
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        
        # Fazer backup se o arquivo existir
        if os.path.exists(self.config_path):
            import shutil
            backup_path = self.config_path + ".bak"
            shutil.copy2(self.config_path, backup_path)
        
        try:
            # Construir dados
            data = {}
            if os.path.exists(self.config_path):
                with open(self.config_path, "r") as f:
                    data = json.load(f)
            
            # Atualizar FFlags
            fflags = {}
            for i in range(self.fflag_store.get_n_items()):
                item = self.fflag_store.get_item(i)
                fflags[item.name] = self.parse_value(item.value)
            data["fflags"] = fflags
            
            # Salvar arquivo
            with open(self.config_path, "w") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
                
            self.show_info("FFlags saved successfully! Backup created.")
            self.update_fflags_text()
            
        except Exception as e:
            self.show_error(f"Error saving config.json: {str(e)}")

    def on_import_fflags(self, button):
        dialog = Gtk.FileChooserDialog(
            title="Select FFlags JSON File",
            transient_for=self,
            modal=True,
            action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("Import", Gtk.ResponseType.OK)

        filter_json = Gtk.FileFilter()
        filter_json.set_name("JSON files")
        filter_json.add_pattern("*.json")
        dialog.add_filter(filter_json)

        def on_response(dlg, response_id):
            if response_id == Gtk.ResponseType.OK:
                file = dlg.get_file()
                if file:
                    try:
                        with open(file.get_path(), "r") as f:
                            data = json.load(f)

                        # Limpar lista atual
                        self.fflag_store.remove_all()

                        # Processar FFlags com correção de vírgulas
                        fflags = data.get("fflags", data)
                        fixed_count = 0
                        corrected_fflags = {}
                        for key, value in fflags.items():
                            orig_key, orig_value = key, str(value)
                            fixed = False
                            # Corrigir vírgula no final do nome
                            if key.endswith(","):
                                key = key.rstrip(",").strip()
                                fixed = True
                            # Corrigir vírgula no final do valor
                            if orig_value.endswith(","):
                                value = orig_value.rstrip(",").strip()
                                fixed = True
                            else:
                                value = orig_value
                            if fixed:
                                fixed_count += 1
                            corrected_fflags[key] = value
                            self.fflag_store.append(FFlagItem(key, value))

                        self.update_fflags_text()
                        self.update_easy_ui_from_fflags(corrected_fflags)
                        msg = f"{len(corrected_fflags)} FFlags imported successfully!"
                        if fixed_count > 0:
                            msg += f"\nTrailing commas detected and fixed in {fixed_count} FFlags."
                        self.show_info(msg)

                        # Salvar automaticamente após importar
                        self.on_save_fflags(None)

                    except Exception as e:
                        self.show_error(f"Failed to import FFlags: {str(e)}")
            dlg.destroy()

        dialog.connect("response", on_response)
        dialog.present()

    def on_apply_easy(self, button):
        # Remover FFlags do acesso fácil que não estão marcadas
        easy_flags = [
            "DFIntTaskSchedulerTargetFps", "DFFlagUseVisBugChecks", "DFFlagDebugRenderForceTechnologyVoxel",
            "FFlagDebugForceFutureIsBrightPhase2", "FFlagDebugForceFutureIsBrightPhase3", "FFlagDebugAvatarChatVisualization",
            "FFlagDebugCheckRenderThreading", "FFlagRenderDebugCheckThreading2", "FIntRuntimeMaxNumOfThreads",
            "FIntTaskSchedulerThreadMin", "FFlagDebugRenderingSetDeterministic", "FIntRomarkStartWithGraphicQualityLevel",
            "FIntTerrainArraySliceSize", "FIntRenderShadowIntensity", "DFFlagDisableDPIScale", "FFlagGlobalWindRendering",
            "FFlagGlobalWindActivated", "FFlagDisablePostFx", "FFlagDebugSkyGray", "FFlagNewLightAttenuation",
            "FFlagFastGPULightCulling3", "DFFlagTextureQualityOverrideEnabled", "DFIntPerformanceControlTextureQualityBestUtility",
            "DFIntTextureCompositorActiveJobs", "FIntFRMMinGrassDistance", "FIntFRMMaxGrassDistance",
            "FIntRenderGrassDetailStrands", "FIntRenderGrassHeightScaler", "DFIntMaxFrameBufferSize",
            "FIntDebugForceMSAASamples", "FIntRenderShadowmapBias", "DFFlagDebugDrawBroadPhaseAABBs", "FIntCameraFarZPlane"
        ]
        for flag in easy_flags:
            self.remove_easy_fflag(flag)

        # Adicionar apenas os marcados
        if self.fps_entry.get_value() > 0:
            self.set_easy_fflag("DFIntTaskSchedulerTargetFps", int(self.fps_entry.get_value()))

        if self.fflag_occlusion.get_active():
            self.set_easy_fflag("DFFlagUseVisBugChecks", "True")

        if self.switch_voxel.get_active():
            self.set_easy_fflag("DFFlagDebugRenderForceTechnologyVoxel", "True")

        if self.switch_shadow.get_active():
            self.set_easy_fflag("FFlagDebugForceFutureIsBrightPhase2", "True")

        if self.switch_future.get_active():
            self.set_easy_fflag("FFlagDebugForceFutureIsBrightPhase3", "True")

        if self.switch_avatar_chat.get_active():
            self.set_easy_fflag("FFlagDebugAvatarChatVisualization", "True")

        # Só salva configurações de threads se o switch estiver ativado
        if self.switch_threads.get_active():
            if self.switch_hyper.get_active():
                self.set_easy_fflag("FFlagDebugCheckRenderThreading", "True")
                self.set_easy_fflag("FFlagRenderDebugCheckThreading2", "True")

            if self.spin_max_threads.get_value() > 0:
                self.set_easy_fflag("FIntRuntimeMaxNumOfThreads", int(self.spin_max_threads.get_value()))

            if self.spin_min_threads.get_value() > 0:
                self.set_easy_fflag("FIntTaskSchedulerThreadMin", int(self.spin_min_threads.get_value()))

        if self.switch_smooth_terrain.get_active():
            self.set_easy_fflag("FFlagDebugRenderingSetDeterministic", "True")

        if self.switch_quality.get_active():
            self.set_easy_fflag("FIntRomarkStartWithGraphicQualityLevel", int(self.spin_quality.get_value()))

        if self.switch_terrain.get_active():
            self.set_easy_fflag("FIntTerrainArraySliceSize", int(self.spin_terrain.get_value()))

        if self.switch_no_shadows.get_active():
            self.set_easy_fflag("FIntRenderShadowIntensity", 0)

        if self.switch_dpi.get_active():
            self.set_easy_fflag("DFFlagDisableDPIScale", "True")

        if self.switch_wind.get_active():
            self.set_easy_fflag("FFlagGlobalWindRendering", "True")
            self.set_easy_fflag("FFlagGlobalWindActivated", "True")

        if self.switch_postfx.get_active():
            self.set_easy_fflag("FFlagDisablePostFx", "True")

        if self.switch_gray_sky.get_active():
            self.set_easy_fflag("FFlagDebugSkyGray", "True")

        if self.switch_light_atten.get_active():
            self.set_easy_fflag("FFlagNewLightAttenuation", "True")

        if self.switch_gpu_culling.get_active():
            self.set_easy_fflag("FFlagFastGPULightCulling3", "True")

        if self.switch_high_tex.get_active():
            self.set_easy_fflag("DFFlagTextureQualityOverrideEnabled", "True")

        if self.spin_low_tex.get_value() >= 0:
            self.set_easy_fflag("DFIntPerformanceControlTextureQualityBestUtility", int(self.spin_low_tex.get_value()))

        if self.switch_no_avatar_tex.get_active():
            self.set_easy_fflag("DFIntTextureCompositorActiveJobs", 0)

        if self.switch_no_grass.get_active():
            self.set_easy_fflag("FIntFRMMinGrassDistance", 0)
            self.set_easy_fflag("FIntFRMMaxGrassDistance", 0)
            self.set_easy_fflag("FIntRenderGrassDetailStrands", 0)
            self.set_easy_fflag("FIntRenderGrassHeightScaler", 0)

        if self.switch_fb.get_active():
            self.set_easy_fflag("DFIntMaxFrameBufferSize", int(self.spin_fb.get_value()))

        if self.switch_msaa.get_active():
            self.set_easy_fflag("FIntDebugForceMSAASamples", int(self.spin_msaa.get_value()))

        if self.switch_bias.get_active():
            self.set_easy_fflag("FIntRenderShadowmapBias", int(self.spin_bias.get_value()))

        if self.switch_outline.get_active():
            self.set_easy_fflag("DFFlagDebugDrawBroadPhaseAABBs", "True")

        if self.switch_xray.get_active():
            self.set_easy_fflag("FIntCameraFarZPlane", 1)

        self.show_info("Settings applied to FFlags!")
        self.on_save_fflags(None)  # Salvar automaticamente

    def show_error(self, message):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            modal=True,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.CLOSE,
            text=message
        )
        dialog.connect("response", lambda d, r: d.destroy())
        dialog.present()

    def show_warning(self, message):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            modal=True,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.OK,
            text=message
        )
        dialog.connect("response", lambda d, r: d.destroy())
        dialog.present()

    def show_info(self, message):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            modal=True,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=message
        )
        dialog.connect("response", lambda d, r: d.destroy())
        dialog.present()

class LukuApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.luku.sober")
        
        # Adicionar estilos CSS
        css_provider = Gtk.CssProvider()
        css = b"""
        .header {
            background-color: rgba(0, 0, 0, 0.8);
            border-radius: 12px;
            padding: 10px;
        }
        .app-title {
            font-size: 18px;
            font-weight: bold;
        }
        .app-subtitle {
            font-size: 12px;
            opacity: 0.8;
        }
        .section-title {
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 15px;
        }
        .suggested-action {
            background-color: @accent_bg_color;
            color: @accent_fg_color;
        }
        """
        css_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def do_activate(self):
        win = LukuWindow(self)
        win.present()

if __name__ == "__main__":
    app = LukuApp()
    app.run()
