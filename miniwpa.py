#!/usr/bin/env python3

import dbus

SUP_DBUS_SERVICE   = "fi.w1.wpa_supplicant1"
SUP_DBUS_OPATH     = "/fi/w1/wpa_supplicant1"

# Fixes for API inconveniences

def unquote(s):
    if not s[0] == s[-1] == '"':
        raise ValueError('String is not quoted: {}'.format(s))
    return s[1:-1]

def do_things(arr, charset='utf-8'):
    # This API should win a prize.
    bs = bytes(b.numerator for b in arr)
    try:
        return bs.decode(charset)
    except UnicodeDecodeError:
        return '<BINARY {}>'.format(bs)

class DBusMixin:
    def __init__(self, parent, path):
        self.parent, self.bus, self.path = parent, parent.bus, path
        self.obj = self.bus.get_object(SUP_DBUS_SERVICE, path)
        self.refresh()

    def refresh(self):
        pass

    def __getitem__(self, key):
        try:
            return self.obj.Get(self.objif, key, dbus_interface=dbus.PROPERTIES_IFACE)
        except dbus.exceptions.DBusException as ex:
            if ex.args[0] == 'No such property':
                raise KeyError(*ex.args, key)
            else:
                raise ex

def list_property(key, rt):
    def getter(self):
        return [ rt(self, path) for path in self[key] ]
    return property(getter)

def simple_property(key, rt=lambda x:x):
    def getter(self):
        if isinstance(rt, type) and issubclass(rt, DBusMixin):
            return rt(self, self[key])
        return rt(self[key])
    return property(getter)

def dict_subprop(attr, key, rt=lambda x:x):
    def getter(self):
        val = getattr(self, attr)[key]
        if isinstance(rt, type) and issubclass(rt, DBusMixin):
            return rt(self, val)
        return rt(val)
    return property(getter)
#dbus.Dictionary({dbus.String('ieee80211w'): dbus.String('3', variant_level=1), dbus.String('beacon_int'): dbus.String('0', variant_level=1), dbus.String('vht_tx_mcs_nss_6'): dbus.String('-1', variant_level=1), dbus.String('priority'): dbus.String('5', variant_level=1), dbus.String('eapol_flags'): dbus.String('3', variant_level=1), dbus.String('vht_rx_mcs_nss_2'): dbus.String('-1', variant_level=1), dbus.String('vht_rx_mcs_nss_6'): dbus.String('-1', variant_level=1), dbus.String('vht_rx_mcs_nss_4'): dbus.String('-1', variant_level=1), dbus.String('mac_addr'): dbus.String('-1', variant_level=1), dbus.String('ca_cert'): dbus.String('"/etc/wpa_supplicant/tubit.pem"', variant_level=1), dbus.String('identity'): dbus.String('"hceline@win.tu-berlin.de"', variant_level=1), dbus.String('disable_vht'): dbus.String('0', variant_level=1), dbus.String('vht_capa'): dbus.String('0', variant_level=1), dbus.String('vht_tx_mcs_nss_8'): dbus.String('-1', variant_level=1), dbus.String('group'): dbus.String('CCMP TKIP', variant_level=1), dbus.String('disable_ht'): dbus.String('0', variant_level=1), dbus.String('ocsp'): dbus.String('0', variant_level=1), dbus.String('frequency'): dbus.String('0', variant_level=1), dbus.String('proactive_key_caching'): dbus.String('-1', variant_level=1), dbus.String('vht_tx_mcs_nss_3'): dbus.String('-1', variant_level=1), dbus.String('erp'): dbus.String('0', variant_level=1), dbus.String('vht_capa_mask'): dbus.String('0', variant_level=1), dbus.String('vht_tx_mcs_nss_7'): dbus.String('-1', variant_level=1), dbus.String('vht_tx_mcs_nss_1'): dbus.String('-1', variant_level=1), dbus.String('vht_rx_mcs_nss_1'): dbus.String('-1', variant_level=1), dbus.String('peerkey'): dbus.String('0', variant_level=1), dbus.String('vht_tx_mcs_nss_5'): dbus.String('-1', variant_level=1), dbus.String('wpa_ptk_rekey'): dbus.String('0', variant_level=1), dbus.String('wep_tx_keyidx'): dbus.String('0', variant_level=1), dbus.String('fragment_size'): dbus.String('1398', variant_level=1), dbus.String('vht_tx_mcs_nss_2'): dbus.String('-1', variant_level=1), dbus.String('ignore_broadcast_ssid'): dbus.String('0', variant_level=1), dbus.String('vht_tx_mcs_nss_4'): dbus.String('-1', variant_level=1), dbus.String('engine2'): dbus.String('0', variant_level=1), dbus.String('sim_num'): dbus.String('1', variant_level=1), dbus.String('ampdu_density'): dbus.String('-1', variant_level=1), dbus.String('engine'): dbus.String('0', variant_level=1), dbus.String('disable_sgi'): dbus.String('0', variant_level=1), dbus.String('ht40_intolerant'): dbus.String('0', variant_level=1), dbus.String('eap'): dbus.String('PEAP', variant_level=1), dbus.String('mode'): dbus.String('0', variant_level=1), dbus.String('mem_only_psk'): dbus.String('0', variant_level=1), dbus.String('mixed_cell'): dbus.String('0', variant_level=1), dbus.String('ssid'): dbus.String('"eduroam"', variant_level=1), dbus.String('key_mgmt'): dbus.String('WPA-EAP IEEE8021X', variant_level=1), dbus.String('vht_rx_mcs_nss_5'): dbus.String('-1', variant_level=1), dbus.String('disabled'): dbus.String('0', variant_level=1), dbus.String('ap_max_inactivity'): dbus.String('0', variant_level=1), dbus.String('vht_rx_mcs_nss_3'): dbus.String('-1', variant_level=1), dbus.String('fixed_freq'): dbus.String('0', variant_level=1), dbus.String('disable_max_amsdu'): dbus.String('-1', variant_level=1), dbus.String('bg_scan_period'): dbus.String('-1', variant_level=1), dbus.String('disable_ht40'): dbus.String('0', variant_level=1), dbus.String('disable_ldpc'): dbus.String('0', variant_level=1), dbus.String('dtim_period'): dbus.String('0', variant_level=1), dbus.String('vht_rx_mcs_nss_7'): dbus.String('-1', variant_level=1), dbus.String('scan_ssid'): dbus.String('0', variant_level=1), dbus.String('proto'): dbus.String('WPA RSN', variant_level=1), dbus.String('pairwise'): dbus.String('CCMP TKIP', variant_level=1), dbus.String('eap_workaround'): dbus.String('-1', variant_level=1), dbus.String('vht_rx_mcs_nss_8'): dbus.String('-1', variant_level=1), dbus.String('ampdu_factor'): dbus.String('-1', variant_level=1)}, signature=dbus.Signature('sv'), variant_level=1)

def obj_method(key, mapper=lambda: None, rt=lambda x:x):
    def wrapper(self, *args, **kwargs):
        res = getattr(self.obj, key)(*mapper(*args, **kwargs), dbus_interface=self.objif)
        if isinstance(rt, type) and issubclass(rt, DBusMixin):
            return rt(self, res)
        return rt(res)
    return wrapper

def filter_none(d):
    return { k: v for k, v in d.items() if v is not None }

# Begin of actual implementation

class ScanResult(DBusMixin):
    objif = "fi.w1.wpa_supplicant1.BSS"
    ssid                    = simple_property('SSID', lambda x: do_things(x, charset='latin-1'))
    bssid                   = simple_property('BSSID',
            lambda x: ':'.join(['{:02x}']*6).format(*[v.numerator for v in x]))
    signal  = signal_dbm    = simple_property('Signal')
    freq    = freq_mhz      = simple_property('Frequency')

    def __repr__(self):
        return '<ScanResult@{}MHz P={}dBm bssid={} ssid="{}">'.format(
                self.freq_mhz, self.signal_dbm, self.bssid, self.ssid)

class Network(DBusMixin):
    objif = "fi.w1.wpa_supplicant1.Network"
    _props  = simple_property('Properties')
    ssid    = dict_subprop('_props', 'ssid', unquote)

    def remove(self):
        parent.obj.RemoveNetwork(self.path)

    def select(self):
        parent.obj.SelectNetwork(self.path)

    def __repr__(self):
        return '<miniwpa.Network "{}">'.format(self.ssid)

class Interface(DBusMixin):
    objif = "fi.w1.wpa_supplicant1.Interface"
    networks        = list_property('Networks', Network)
    scan_results    = list_property('BSSs',     ScanResult)
    current_bss     = simple_property('CurrentBSS',         ScanResult)
    current_net     = simple_property('CurrentNetwork',     Network)
    scanning        = simple_property('Scanning',           bool)
    current_auth    = simple_property('CurrentAuthMode',    str)
    name            = simple_property('Ifname',             str)
    disconnect      = obj_method('Disconnect')
    add_net         = obj_method('AddNetwork', lambda **kwargs: kwargs, rt=Network)
    reassoc         = obj_method('Reassociate')
    reattach        = obj_method('Reattach')
    reconnect       = obj_method('Reconnect')
    signal          = obj_method('SignalPoll')
    scan            = obj_method('Scan', lambda scantype='active', ssids=None, ies=None, chs=None, allowRoam=True:
        (dbus.Dictionary(filter_none(
            {'Type': scantype,
             'AllowRoam': allowRoam,
             'SSIDs': ssids,
             'IEs': ies,
             'Channels': chs}), signature='sv'),))

    def __repr__(self):
        return '<miniwpa.Interface {}>'.format(self.name)

class WPASupplicant(DBusMixin):
    objif = 'fi.w1.wpa_supplicant1'
    interfaces      = list_property('Interfaces', Interface)
    get_interface   = obj_method('GetInterface', Interface)

    def __init__(self):
        self.bus = dbus.SystemBus()
        self.obj = self.bus.get_object(SUP_DBUS_SERVICE, SUP_DBUS_OPATH)
    
    @property
    def if_dict(self):
        return { iface.name: iface for iface in self.interfaces }

