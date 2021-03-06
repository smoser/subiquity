# Copyright 2015 Canonical, Ltd.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
from urwid import Text, CheckBox

from subiquitycore.view import BaseView
from subiquitycore.ui.buttons import cancel_btn, done_btn
from subiquitycore.ui.container import Columns, ListBox, Pile
from subiquitycore.ui.interactive import UsernameEditor
from subiquitycore.ui.utils import Color, Padding

from subiquity.models.filesystem import humanize_size


log = logging.getLogger('subiquitycore.ui.lvm')


class LVMVolumeGroupView(BaseView):
    def __init__(self, model, signal):
        self.model = model
        self.signal = signal
        self.volgroup = UsernameEditor()
        self.selected_disks = []
        body = [
            Padding.center_50(self._build_disk_selection()),
            Padding.line_break(""),
            Padding.center_50(self._build_lvm_configuration()),
            Padding.line_break(""),
            Padding.fixed_10(self._build_buttons())
        ]
        super().__init__(ListBox(body))

    def _build_disk_selection(self):
        log.debug('lvm: _build_disk_selection')
        items = [
            Text("DISK SELECTION")
        ]

        # lvm can use empty whole disks, or empty partitions
        avail_disks = self.model.get_empty_disk_names()
        avail_parts = self.model.get_empty_partition_names()
        avail_devs = sorted(avail_disks + avail_parts)
        if len(avail_devs) == 0:
            return items.append(
                [Color.info_minor(Text("No available disks."))])

        for dname in avail_devs:
            device = self.model.get_disk(dname)
            if device.path != dname:
                # we've got a partition
                lvmdev = device.get_partition(dname)
            else:
                lvmdev = device

            disk_sz = humanize_size(lvmdev.size)
            disk_string = "{}     {},     {}".format(dname,
                                                     disk_sz,
                                                     device.model)
            log.debug('lvm: disk_string={}'.format(disk_string))
            self.selected_disks.append(CheckBox(disk_string))

        items += self.selected_disks

        return Pile(items)

    def _build_lvm_configuration(self):
        log.debug('lvm: _build_lvm_config')
        items = [
            Text("LVM VOLUMEGROUP CONFIGURATION"),
            Columns(
                [
                    ("weight", 0.2, Text("VolumeGroup Name",
                                         align="right")),
                    ("weight", 0.3,
                     Color.string_input(self.volgroup))
                ],
                dividechars=4
            ),
        ]
        return Pile(items)

    def _build_buttons(self):
        log.debug('lvm: _build_buttons')
        cancel = cancel_btn(on_press=self.cancel)
        done = done_btn(on_press=self.done)

        buttons = [
            Color.button(done),
            Color.button(cancel)
        ]
        return Pile(buttons)

    def done(self, result):
        result = {
            'devices': [x.get_label() for x in self.selected_disks if x.state],
            'volgroup': self.volgroup.value,
        }
        log.debug('lvm_done: result = {}'.format(result))
        self.model.add_lvm_volgroup(result)
        self.signal.prev_signal()

    def cancel(self, button):
        log.debug('lvm: button_cancel')
        self.signal.prev_signal()


class AddLVMPartitionView(BaseView):
    pass
