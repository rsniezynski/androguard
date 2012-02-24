#!/usr/bin/env python

# This file is part of Androguard.
#
# Copyright (C) 2012, Anthony Desnos <desnos at t0t0.fr>
# All rights reserved.
#
# Androguard is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Androguard is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Androguard.  If not, see <http://www.gnu.org/licenses/>.

import sys

from optparse import OptionParser

from androguard.core.androgen import Androguard
from androguard.core import androconf
from androguard.core.analysis import diff

option_0 = { 'name' : ('-i', '--input'), 'help' : 'file : use these filenames', 'nargs' : 2 }
option_1 = { 'name' : ('-j', '--json'), 'help' : 'file : use json file', 'nargs' : 2 }
option_2 = { 'name' : ('-d', '--display'), 'help' : 'display the file in human readable format', 'action' : 'count' }
option_3 = { 'name' : ('-v', '--version'), 'help' : 'version of the API', 'action' : 'count' }

options = [option_0, option_1, option_2, option_3]

def main(options, arguments) :
    if options.input != None :
        a = Androguard( options.input )
        a.ianalyze()

        vm1 = a.get_bc()[0][1].get_vm()
        vmx1 = a.get_bc()[0][1].get_analysis()

        vm2 = a.get_bc()[1][1].get_vm()
        vmx2 = a.get_bc()[1][1].get_analysis()

        dsim = diff.Sim( [ vm1, vmx1 ], [ vm2, vmx2 ] )
        dsim.show()

        if options.display :
            print "SIMILAR methods:"
            diff_methods = dsim.get_diff_methods()
            for i in diff_methods :
                i.show2()
            
            print "IDENTICAL methods:"
            new_methods = dsim.get_match_methods()
            for i in new_methods :
                i.show2()

            print "NEW methods:"
            new_methods = dsim.get_new_methods()
            for i in new_methods :
                i.show2()

            print "DELETED methods:"
            del_methods = dsim.get_delete_methods()
            for i in del_methods :
                i.show2()

    # Not yet usable
    elif options.json != None :
        a = Androguard( [ options.json[0] ] )
        a.ianalyze()
       
        vm1 = a.get_bc()[0][1].get_vm()
        vmx1 = a.get_bc()[0][1].get_analysis()

        diff.SimJson( [ vm1, vmx1 ], options.json[1] )

    elif options.version != None :
        print "Androsim version %s" % androconf.ANDROGUARD_VERSION

if __name__ == "__main__" :
    parser = OptionParser()
    for option in options :
        param = option['name']
        del option['name']
        parser.add_option(*param, **option)

    options, arguments = parser.parse_args()
    sys.argv[:] = arguments
    main(options, arguments)