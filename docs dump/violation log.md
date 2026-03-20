
void ViolationLog(void)

{
  longlong *plVar1;
  int iVar2;
  void *_Src;
  undefined8 *puVar3;
  longlong *plVar4;
  undefined8 *puVar5;
  int iVar6;
  longlong lVar7;
  undefined1 auStack_d8 [32];
  undefined8 local_b8;
  int local_b0 [2];
  undefined8 local_a8;
  undefined8 local_a0;
  undefined8 local_98;
  undefined8 local_90;
  undefined8 local_88;
  undefined8 local_80;
  undefined8 local_78;
  undefined8 local_70;
  undefined8 local_68;
  undefined8 local_60;
  undefined8 local_58;
  undefined8 local_50;
  longlong local_48 [4];
  
  local_48[2] = DAT_1446f59e8 ^ (ulonglong)auStack_d8;
  if ((*(int *)(*(longlong *)((longlong)ThreadLocalStoragePointer + (ulonglong)_tls_index * 8) + 4)
       < DAT_14479c028) && (_Init_thread_header(&DAT_14479c028), DAT_14479c028 == -1)) {
    local_b8 = 0;
    local_b0[0] = 0xd;
    local_b0[1] = 0;
    FUN_140503dc0(&local_b8,0);
    CopyParam2IntoParam1(local_b8,L"Team Killing",0x1a);
    local_a8 = 0;
    local_a0 = 0x1b;
    FUN_140503dc0(&local_a8,0);
    CopyParam2IntoParam1(local_a8,L"Damaging Friendly Vehicles",0x36);
    local_98 = 0;
    local_90 = 0x1d;
    FUN_140503dc0(&local_98,0);
    CopyParam2IntoParam1(local_98,L"Damaging Friendly Structures",0x3a);
    local_88 = 0;
    local_80 = 0x1f;
    FUN_140503dc0(&local_88,0);
    CopyParam2IntoParam1(local_88,L"Suspected Exploiting / Hacking",0x3e);
    local_78 = 0;
    local_70 = 0x13;
    FUN_140503dc0(&local_78,0);
    CopyParam2IntoParam1(local_78,L"Offensive Language",0x26);
    local_68 = 0;
    local_60 = 0x1f;
    FUN_140503dc0(&local_68,0);
    CopyParam2IntoParam1(local_68,L"Disruptive Structure Placement",0x3e);
    local_58 = 0;
    local_50 = 0x12;
    FUN_140503dc0(&local_58,0);
    CopyParam2IntoParam1(local_58,L"Intelligence Leak",0x24);
    local_48[0] = 0;
    local_48[1] = 0x16;
    FUN_140503dc0(local_48,0);
    CopyParam2IntoParam1(local_48[0],L"Suspected Alt Account",0x2c);
    DAT_14479c018 = (undefined8 *)0x0;
    lVar7 = 8;
    DAT_14479c020 = 8;
    FUN_140514040(&DAT_14479c018,8,0);
    puVar5 = &local_b8;
    iVar6 = 8;
    puVar3 = DAT_14479c018;
    do {
      *puVar3 = 0;
      iVar2 = *(int *)(puVar5 + 1);
      _Src = (void *)*puVar5;
      *(int *)(puVar3 + 1) = iVar2;
      if (iVar2 == 0) {
        *(undefined4 *)((longlong)puVar3 + 0xc) = 0;
      }
      else {
        FUN_1405140b0(puVar3,iVar2,0);
        memcpy((void *)*puVar3,_Src,(longlong)iVar2 * 2);
      }
      puVar3 = puVar3 + 2;
      puVar5 = puVar5 + 2;
      iVar6 = iVar6 + -1;
    } while (iVar6 != 0);
    plVar4 = local_48 + 2;
    do {
      plVar1 = plVar4 + -2;
      plVar4 = plVar4 + -2;
      lVar7 = lVar7 + -1;
      if (*plVar1 != 0) {
        FUN_14125c6c0();
      }
    } while (lVar7 != 0);
    atexit((_func_5014 *)&LAB_14326cfe0);
    _Init_thread_footer(&DAT_14479c028);
  }
  FUN_143230010(local_48[2] ^ (ulonglong)auStack_d8);
  return;
}

