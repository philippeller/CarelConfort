#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import minimalmodbus

class carelConfort(object):
    registers = {'lastTemp':2,
                'currentTemp':3,
                'setPoint':13,
                'highTemp':18,
                'lowTemp':19,
                'dAlarmHigh':24,
                'dAlarmLow':25
                }
    coils = {'door':6,
            'compressor':0
            }

    def __init__(self,port='/dev/ttyUSB0',address=1,baudrate=9600,parity='E'):
        self.interface = minimalmodbus.Instrument(port,address)
        self.interface.serial.baudrate = baudrate
        self.interface.serial.parity = parity

    def __getattr__(self,attr):
        if self.registers.has_key(attr):
            return self._read_register(self.registers[attr])
        elif self.coils.has_key(attr):
            return self._read_coil(self.coils[attr])
        else:
            try:
                super(carelConfort, self).__getattr__(attr)
            except AttributeError:
                raise Exception('Instance has no attribute %s'%attr)

    def __setattr__(self,attr,value):
        if self.registers.has_key(attr):
            return self._write_register(self.registers[attr],value)
        elif self.coils.has_key(attr):
            raise Exception('cannot write to function code 1')
        else:
            super(carelConfort, self).__setattr__(attr,value)

    def _read_register(self,register):
        return self.interface.read_register(register,signed=True,functioncode=3)

    def _write_register(self,register,value):
        try:
            return self.interface.write_register(register,value,signed=True,functioncode=6)
        except ValueError:
            raise Exception('Cannot write on register %s'%register)

    def _read_coil(self,coil):
        return self.interface.read_bit(coil,functioncode=1)

if __name__=='__main__':
    freezer = carelConfort()
    temp = freezer.currentTemp/10.
    print 'temperature = %s degC'%temp
