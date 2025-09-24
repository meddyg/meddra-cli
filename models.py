from typing import Any, List, Optional, ClassVar, Dict

from sqlalchemy import BigInteger, DateTime, Index, Integer, Numeric, PrimaryKeyConstraint,  String, Text, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import datetime
import decimal

EXCLUDED_COLUMNS = {'id', 'language', 'version', 'created_at', 'updated_at'}

class Base(DeclarativeBase):
    __table_args__: Dict[str, Any] = {'schema': 'meddra' }

class MeddraChangesMeddraToSnomed(Base):
    __tablename__ = 'meddra_changes_meddra_to_snomed'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='meddra_changes_meddra_to_snomed_pk'),
        Index('meddra_changes_meddra_to_snomed_meddra_code_new_mapping_index', 'meddra_code_new_mapping'),
        Index('meddra_changes_meddra_to_snomed_meddra_code_original_mapping_in', 'meddra_code_original_mapping'),
        Index('meddra_changes_meddra_to_snomed_snomed_ct_code_new_mapping_inde', 'snomed_ct_code_new_mapping'),
        Index('meddra_changes_meddra_to_snomed_snomed_ct_code_original_mapping', 'snomed_ct_code_original_mapping'),
        Index('meddra_changes_meddra_to_snomed_version_impact_index', 'version_impact'),
        Index('meddra_changes_meddra_to_snomed_version_index', 'version')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    meddra_code_new_mapping: Mapped[int] = mapped_column(Integer)
    meddra_llt_new_mapping: Mapped[str] = mapped_column(String(100))
    snomed_ct_code_new_mapping: Mapped[int] = mapped_column(Integer)
    snomed_ct_fsn_new_mapping: Mapped[str] = mapped_column(String(100))
    meddra_code_original_mapping: Mapped[int] = mapped_column(Integer)
    snomed_ct_code_original_mapping: Mapped[int] = mapped_column(Integer)
    snomed_ct_fsn_original_mapping: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    version_impact: Mapped[Optional[int]] = mapped_column(Integer)
    meddra_llt_original_mapping: Mapped[Optional[str]] = mapped_column(String(100))
    language: Mapped[Optional[str]] = mapped_column(String(8))
    version: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(5, 2))


class MeddraChangesSnomedToMeddra(Base):
    __tablename__ = 'meddra_changes_snomed_to_meddra'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='meddra_changes_snomed_to_meddra_pk'),
        Index('meddra_changes_snomed_to_meddra_meddra_code_new_mapping_index', 'meddra_code_new_mapping'),
        Index('meddra_changes_snomed_to_meddra_meddra_code_original_mapping_in', 'meddra_code_original_mapping'),
        Index('meddra_changes_snomed_to_meddra_snomed_ct_code_new_mapping_inde', 'snomed_ct_code_new_mapping'),
        Index('meddra_changes_snomed_to_meddra_snomed_ct_code_original_mapping', 'snomed_ct_code_original_mapping'),
        Index('meddra_changes_snomed_to_meddra_version_impact_index', 'version_impact'),
        Index('meddra_changes_snomed_to_meddra_version_index', 'version')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    snomed_ct_code_new_mapping: Mapped[int] = mapped_column(Integer)
    snomed_ct_fsn_new_mapping: Mapped[str] = mapped_column(String(100))
    meddra_code_new_mapping: Mapped[int] = mapped_column(Integer)
    meddra_llt_new_mapping: Mapped[str] = mapped_column(String(100))
    snomed_ct_code_original_mapping: Mapped[int] = mapped_column(Integer)
    snomed_ct_fsn_original_mapping: Mapped[str] = mapped_column(String(100))
    meddra_code_original_mapping: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    version_impact: Mapped[Optional[int]] = mapped_column(Integer)
    meddra_llt_original_mapping: Mapped[Optional[str]] = mapped_column(String(100))
    language: Mapped[Optional[str]] = mapped_column(String(8))
    version: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(5, 2))


class MeddraHistory(Base):
    __tablename__ = 'meddra_history'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='meddra_history_pk'),
        Index('meddra_history_version_index', 'version')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    term_code: Mapped[int] = mapped_column(Integer)
    term_name: Mapped[str] = mapped_column(String(100))
    term_addition_version: Mapped[str] = mapped_column(String(5))
    term_type: Mapped[str] = mapped_column(String(4))
    action: Mapped[str] = mapped_column(String(1))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    llt_currency: Mapped[Optional[str]] = mapped_column(String(1))
    language: Mapped[Optional[str]] = mapped_column(String(8))
    version: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(5, 2))


class MeddraHlgtHltComp(Base):
    __tablename__ = 'meddra_hlgt_hlt_comp'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='meddra_hlgt_hlt_comp_pk'),
        Index('ix1_hlgt_hlt01', 'hlgt_code', 'hlt_code'),
        Index('ix1_hlgt_hlt02', 'hlt_code', 'hlgt_code')
    )

    __meddra_file_info__ = {
        'filename': 'hlgt_hlt.asc',
        '_column_order': ['hlgt_code', 'hlt_code']
    }

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    hlgt_code: Mapped[Optional[int]] = mapped_column(Numeric(10,2))
    hlt_code: Mapped[Optional[int]] = mapped_column(Numeric(10,2))
    
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    language: Mapped[Optional[str]] = mapped_column(String(8))
    version: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(5, 2))


class MeddraHlgtPrefTerm(Base):
    __tablename__ = 'meddra_hlgt_pref_term'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='meddra_hlgt_pref_term_pk'),
        Index('ix1_hlgt01', 'hlgt_code'),
        Index('ix1_hlgt02', 'hlgt_name'),
        Index('ix1_hlgt03', 'version')
    )

    __meddra_file_info__ = {
        'filename': 'hlgt.asc',
        '_column_order': [
            'hlgt_code', 
            'hlgt_name',
            'hlgt_whoart_code', 
            'hlgt_harts_code', 
            'hlgt_costart_sym',
            'hlgt_icd9_code', 
            'hlgt_icd9cm_code', 
            'hlgt_icd10_code', 
            'hlgt_jart_code'
        ]
    }

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    hlgt_code: Mapped[Optional[int]] = mapped_column(Numeric(10,2))
    hlgt_name: Mapped[Optional[str]] = mapped_column(String(100))
    hlgt_whoart_code: Mapped[Optional[str]] = mapped_column(String(7), comment='A partir de la versión 15.0 de MedDRA, estos campos no contienen datos.')
    hlgt_harts_code: Mapped[Optional[int]] = mapped_column(Numeric(10,2), comment='A partir de la versión 15.0 de MedDRA, estos campos no contienen datos.')
    hlgt_costart_sym: Mapped[Optional[str]] = mapped_column(String(21), comment='A partir de la versión 15.0 de MedDRA, estos campos no contienen datos.')
    hlgt_icd9_code: Mapped[Optional[str]] = mapped_column(String(8), comment='A partir de la versión 15.0 de MedDRA, estos campos no contienen datos.')
    hlgt_icd9cm_code: Mapped[Optional[str]] = mapped_column(String(8), comment='A partir de la versión 15.0 de MedDRA, estos campos no contienen datos.')
    hlgt_icd10_code: Mapped[Optional[str]] = mapped_column(String(8), comment='A partir de la versión 15.0 de MedDRA, estos campos no contienen datos.')
    hlgt_jart_code: Mapped[Optional[str]] = mapped_column(String(6), comment='A partir de la versión 15.0 de MedDRA, estos campos no contienen datos.')
    
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    language: Mapped[Optional[str]] = mapped_column(String(8))
    version: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(5, 2))


class MeddraHltPrefComp(Base):
    __tablename__ = 'meddra_hlt_pref_comp'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='meddra_hlt_pref_comp_pk'),
        Index('ix1_hlt_pt01', 'hlt_code', 'pt_code'),
        Index('ix1_hlt_pt02', 'pt_code', 'hlt_code'),
        Index('ix1_hlt_pt03', 'version')
    )

    __meddra_file_info__ = {
        'filename': 'hlt_pt.asc',
        '_column_order': ['hlt_code', 'pt_code']
    }

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    hlt_code: Mapped[Optional[int]] = mapped_column(Numeric(10,2))
    pt_code: Mapped[Optional[int]] = mapped_column(Numeric(10,2))

    language: Mapped[Optional[str]] = mapped_column(String(8))
    version: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(5, 2))


class MeddraHltPrefTerm(Base):
    __tablename__ = 'meddra_hlt_pref_term'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='meddra_hlt_pref_term_pk'),
        Index('ix1_hlt01', 'hlt_code'),
        Index('ix1_hlt02', 'hlt_name'),
        Index('ix1_hlt03', 'version')
    )

    __meddra_file_info__ = {
        'filename': 'hlt.asc',
        '_column_order': [
            'hlt_code', 
            'hlt_name',
            'hlt_whoart_code', 
            'hlt_harts_code', 
            'hlt_costart_sym',
            'hlt_icd9_code', 
            'hlt_icd9cm_code', 
            'hlt_icd10_code', 
            'hlt_jart_code'
        ]
    }

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    hlt_code: Mapped[int] = mapped_column(Numeric(10,2))
    hlt_name: Mapped[str] = mapped_column(String(100))

    hlt_whoart_code: Mapped[Optional[str]] = mapped_column(String(7), comment='A partir de la versión 15.0 de MedDRA, estos campos no contienen datos.')
    hlt_harts_code: Mapped[Optional[int]] = mapped_column(Numeric(10,2), comment='A partir de la versión 15.0 de MedDRA, estos campos no contienen datos.')
    hlt_costart_sym: Mapped[Optional[str]] = mapped_column(String(21), comment='A partir de la versión 15.0 de MedDRA, estos campos no contienen datos.')
    hlt_icd9_code: Mapped[Optional[str]] = mapped_column(String(8), comment='A partir de la versión 15.0 de MedDRA, estos campos no contienen datos.')
    hlt_icd9cm_code: Mapped[Optional[str]] = mapped_column(String(8), comment='A partir de la versión 15.0 de MedDRA, estos campos no contienen datos.')
    hlt_icd10_code: Mapped[Optional[str]] = mapped_column(String(8), comment='A partir de la versión 15.0 de MedDRA, estos campos no contienen datos.')
    hlt_jart_code: Mapped[Optional[str]] = mapped_column(String(6), comment='A partir de la versión 15.0 de MedDRA, estos campos no contienen datos.')
    
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    language: Mapped[Optional[str]] = mapped_column(String(8))
    version: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(5, 2), comment='MedDRA version')


class MeddraLowLevelTerm(Base):
    __tablename__ = 'meddra_low_level_term'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='meddra_low_level_term_pk'),
        Index('ix1_pt_llt01', 'llt_code'),
        Index('ix1_pt_llt02', 'llt_name'),
        Index('ix1_pt_llt03', 'pt_code'),
        Index('ix1_pt_llt04', 'version')
    )
    __meddra_file_info__: ClassVar[Dict[str, str]] = {
        'filename': 'llt.asc',
        '_column_order': [
            'llt_code',
            'llt_name',
            'pt_code',
            'llt_whoart_code',
            'llt_harts_code',
            'llt_costart_sym',
            'llt_icd9_code',
            'llt_icd9cm_code',
            'llt_icd10_code',
            'llt_currency',
            'llt_jart_code',
        ] # This is the order to load the csv file
    }

    id: Mapped[int] = mapped_column(Numeric(10,2), primary_key=True)
    llt_code: Mapped[int] = mapped_column(BigInteger)
    llt_name: Mapped[str] = mapped_column(String(100))
    pt_code: Mapped[Optional[int]] = mapped_column(BigInteger)
    llt_whoart_code: Mapped[Optional[str]] = mapped_column(String(7), comment='A partir de la versión 15.0 de MedDRA, estos campos no contienen datos')
    llt_harts_code: Mapped[Optional[int]] = mapped_column(Numeric(10,2), comment='A partir de la versión 15.0 de MedDRA, estos campos no contienen datos')
    llt_costart_sym: Mapped[Optional[str]] = mapped_column(String(21), comment='A partir de la versión 15.0 de MedDRA, estos campos no contienen datos')
    llt_icd9_code: Mapped[Optional[str]] = mapped_column(String(8), comment='A partir de la versión 15.0 de MedDRA, estos campos no contienen datos.')
    llt_icd9cm_code: Mapped[Optional[str]] = mapped_column(String(8), comment='A partir de la versión 15.0 de MedDRA, estos campos no contienen datos.')
    llt_icd10_code: Mapped[Optional[str]] = mapped_column(String(8), comment='A partir de la versión 15.0 de MedDRA, estos campos no contienen datos.')
    llt_currency: Mapped[Optional[str]] = mapped_column(String(1))
    llt_jart_code: Mapped[Optional[str]] = mapped_column(String(6), comment='A partir de la versión 15.0 de MedDRA, estos campos no contienen datos.')
    
    # Extra metadata 
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    language: Mapped[Optional[str]] = mapped_column(String(8))
    version: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(5, 2))


class MeddraMapMeddraToSnomed(Base):
    __tablename__ = 'meddra_map_meddra_to_snomed'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='meddra_map_meddra_to_snomed_pk'),
        Index('meddra_map_meddra_to_snomed_meddra_code_index', 'meddra_code'),
        Index('meddra_map_meddra_to_snomed_snomed_ct_code_index', 'snomed_ct_code')
        #Index('meddra_map_meddra_to_snomed_version_index', 'version')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    meddra_code: Mapped[str] = mapped_column(String(20))
    # meddra_llt: Mapped[str] = mapped_column(String(100))
    snomed_ct_code: Mapped[str] = mapped_column(String(20))
    # snomed_ct_fsn: Mapped[Optional[str]] = mapped_column(String(100))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    # language: Mapped[Optional[str]] = mapped_column(String(8))
    # version: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(5, 2))


class MeddraMapSnomedToMeddra(Base):
    __tablename__ = 'meddra_map_snomed_to_meddra'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='meddra_map_snomed_to_meddra_pk'),
        Index('meddra_map_snomed_to_meddra_meddra_code_index', 'meddra_code'),
        Index('meddra_map_snomed_to_meddra_snomed_ct_code_index', 'snomed_ct_code')
        #Index('meddra_map_snomed_to_meddra_version_index', 'version')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    snomed_ct_code: Mapped[str] = mapped_column(String(20))
    # snomed_ct_fsn: Mapped[Optional[str]] = mapped_column(String(100))
    meddra_code: Mapped[str] = mapped_column(String(20))
    # meddra_llt: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    # language: Mapped[Optional[str]] = mapped_column(String(8))
    # version: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(5, 2))


class MeddraMdHierarchy(Base):
    __tablename__ = 'meddra_md_hierarchy'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='meddra_md_hierarchy_pk'),
        Index('ix1_md_hier01', 'pt_code'),
        Index('ix1_md_hier02', 'hlt_code'),
        Index('ix1_md_hier03', 'hlgt_code'),
        Index('ix1_md_hier04', 'soc_code'),
        Index('ix1_md_hier05', 'pt_soc_code')
    )
    
    __meddra_file_info__ = {
        'filename': 'mdhier.asc',
        '_column_order': [
            'pt_code', 
            'hlt_code',
            'hlgt_code', 
            'soc_code',
            'pt_name', 
            'hlt_name',
            'hlgt_name',
            'soc_name',
            'soc_abbrev',
            'null_field', 
            'pt_soc_code', 
            'primary_soc_fg'
        ]
    }

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    pt_code: Mapped[int] = mapped_column(BigInteger)
    hlt_code: Mapped[int] = mapped_column(BigInteger)
    hlgt_code: Mapped[int] = mapped_column(BigInteger)
    soc_code: Mapped[int] = mapped_column(BigInteger)
    pt_name: Mapped[str] = mapped_column(String(100))
    hlt_name: Mapped[str] = mapped_column(String(100))
    hlgt_name: Mapped[str] = mapped_column(String(100))
    soc_name: Mapped[str] = mapped_column(String(100))
    soc_abbrev: Mapped[str] = mapped_column(String(5))
    null_field: Mapped[Optional[str]] = mapped_column(String(10))
    pt_soc_code: Mapped[Optional[int]] = mapped_column(BigInteger) 
    primary_soc_fg: Mapped[Optional[str]] = mapped_column(String(10))

    language: Mapped[Optional[str]] = mapped_column(String(8))
    version: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(5, 2))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))


class MeddraPrefTerm(Base):
    __tablename__ = 'meddra_pref_term'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='meddra_pref_term_pk'),
        Index('ix1_pt01', 'pt_code'),
        Index('ix1_pt02', 'pt_name'),
        Index('ix1_pt03', 'pt_soc_code'),
        Index('ix1_pt04', 'version')
    )

    __meddra_file_info__ = {
        'filename': 'pt.asc',
        '_column_order': [
            'pt_code', 'pt_name', 'null_field', 'pt_soc_code',
            'pt_whoart_code', 'pt_harts_code', 'pt_costart_sym',
            'pt_icd9_code', 'pt_icd9cm_code', 'pt_icd10_code', 'pt_jart_code'
        ]
    }

    id: Mapped[int] = mapped_column(Numeric(10,2), primary_key=True)
    pt_code: Mapped[int] = mapped_column(Integer)
    pt_name: Mapped[Optional[str]] = mapped_column(String(100))
    null_field: Mapped[Optional[str]] = mapped_column(String(10))
    pt_soc_code: Mapped[Optional[int]] = mapped_column(Numeric(10,2))
    pt_whoart_code: Mapped[Optional[str]] = mapped_column(String(7), comment='A partir de la versión 15.0 de MedDRA, estos campos no contienen datos.')
    pt_harts_code: Mapped[Optional[int]] = mapped_column(Numeric(10,2), comment='A partir de la versión 15.0 de MedDRA, estos campos no contienen datos.')
    pt_costart_sym: Mapped[Optional[str]] = mapped_column(String(21), comment='A partir de la versión 15.0 de MedDRA, estos campos no contienen datos.')
    pt_icd9_code: Mapped[Optional[str]] = mapped_column(String(8), comment='A partir de la versión 15.0 de MedDRA, estos campos no contienen datos.')
    pt_icd9cm_code: Mapped[Optional[str]] = mapped_column(String(8), comment='A partir de la versión 15.0 de MedDRA, estos campos no contienen datos.')
    pt_icd10_code: Mapped[Optional[str]] = mapped_column(String(8), comment='A partir de la versión 15.0 de MedDRA, estos campos no contienen datos.')
    pt_jart_code: Mapped[Optional[str]] = mapped_column(String(6), comment='A partir de la versión 15.0 de MedDRA, estos campos no contienen datos.')
    
    # metadata
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    language: Mapped[Optional[str]] = mapped_column(String(8))
    version: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(5, 2), comment='MedDRA version')


class MeddraRelease(Base):
    __tablename__ = 'meddra_release'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='meddra_release_pk'),
        Index('meddra_release_meddra_version_index', 'meddra_version')
    )
    
    __meddra_file_info__ = {
        'filename': 'meddra_release.asc',
        '_column_order': [
            'meddra_version', 'language_version',
            'null_field_a', 'null_field_b', 'null_field_c'
        ]
    }

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    meddra_version: Mapped[str] = mapped_column(String(100))
    language_version: Mapped[str] = mapped_column(String(100))

    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    null_field_a: Mapped[Optional[str]] = mapped_column(String(100))
    null_field_b: Mapped[Optional[str]] = mapped_column(String(100))
    null_field_c: Mapped[Optional[str]] = mapped_column(String(100))

    language: Mapped[Optional[str]] = mapped_column(String(8))
    version: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(5, 2))


class MeddraSmqContent(Base):
    __tablename__ = 'meddra_smq_content'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='meddra_smq_content_pk'),
        Index('ix1_smq_content01', 'smq_code'),
        Index('ix1_smq_content02', 'term_code'),
        Index('ix1_smq_content03', 'version')
    )
    
    __meddra_file_info__ = {
        'filename': 'smq_content.asc',
        '_column_order': [
            'smq_code', 
            'term_code',
            'term_level', 
            'term_scope',
            'term_category',
            'term_weight',
            'term_status',
            'term_addition_version',
            'term_last_modified_version'
        ]
    }
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    smq_code: Mapped[int] = mapped_column(BigInteger)
    term_code: Mapped[int] = mapped_column(BigInteger)
    term_level: Mapped[int] = mapped_column(Integer)
    term_scope: Mapped[int] = mapped_column(Integer)
    term_category: Mapped[str] = mapped_column(String(1))
    term_weight: Mapped[int] = mapped_column(Integer)
    term_status: Mapped[str] = mapped_column(String(1))
    term_addition_version: Mapped[str] = mapped_column(String(5))
    term_last_modified_version: Mapped[str] = mapped_column(String(5))

    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    language: Mapped[Optional[str]] = mapped_column(String(8))
    version: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(5, 2))


class MeddraSmqList(Base):
    __tablename__ = 'meddra_smq_list'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='meddra_smq_list_pk'),
        Index('ix1_smq_list01', 'smq_code')
    )
    
    __meddra_file_info__ = {
        'filename': 'smq_list.asc',
        '_column_order': [
            'smq_code', 
            'smq_name', 
            'smq_level',
            'smq_description',
            'smq_source',
            'smq_note', 
            'meddra_version',
            'status', 
            'smq_algorithm'
        ]
    }

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    smq_code: Mapped[int] = mapped_column(BigInteger)
    smq_name: Mapped[str] = mapped_column(String(100))
    smq_level: Mapped[int] = mapped_column(BigInteger)
    smq_description: Mapped[str] = mapped_column(Text)
    smq_source: Mapped[Optional[str]] = mapped_column(Text)
    smq_note: Mapped[Optional[str]] = mapped_column(Text)
    meddra_version: Mapped[str] = mapped_column(String(5))
    status: Mapped[str] = mapped_column(String(1))
    smq_algorithm: Mapped[str] = mapped_column(Text)

    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    language: Mapped[Optional[str]] = mapped_column(String(8))
    version: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(5, 2))


class MeddraSocHlgtComp(Base):
    __tablename__ = 'meddra_soc_hlgt_comp'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='meddra_soc_hlgt_comp_pk'),
        Index('ix1_soc_hlgt01', 'soc_code', 'hlgt_code'),
        Index('ix1_soc_hlgt02', 'soc_code'),
        Index('ix1_soc_hlgt03', 'hlgt_code', 'soc_code'),
        Index('ix1_soc_hlgt04', 'version')
    )
    
    __meddra_file_info__ = {
        'filename': 'soc_hlgt.asc',
        '_column_order': ['soc_code', 'hlgt_code']
    }

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    soc_code: Mapped[Optional[int]] = mapped_column(BigInteger)
    hlgt_code: Mapped[Optional[int]] = mapped_column(BigInteger)
    
    language: Mapped[Optional[str]] = mapped_column(String(8))
    version: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(5, 2))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))


class MeddraSocIntlOrder(Base):
    __tablename__ = 'meddra_soc_intl_order'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='meddra_soc_intl_order_pk'),
        Index('ix1_intl_ord01', 'intl_ord_code', 'soc_code'),
        Index('ix1_intl_ord02', 'version')
    )

    __meddra_file_info__ = {
        'filename': 'intl_ord.asc',
        '_column_order': ['intl_ord_code', 'soc_code']
    }

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    intl_ord_code: Mapped[int] = mapped_column(BigInteger)
    soc_code: Mapped[int] = mapped_column(BigInteger)

    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    language: Mapped[Optional[str]] = mapped_column(String(8))
    version: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(5, 2))


class MeddraSocTerm(Base):
    __tablename__ = 'meddra_soc_term'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='meddra_soc_term_pk'),
        Index('ix1_soc01', 'soc_code'),
        Index('ix1_soc02', 'soc_name'),
        Index('ix1_soc03', 'version')
    )

    __meddra_file_info__ = {
        'filename': 'soc.asc',
        '_column_order': [
            'soc_code', 
            'soc_name', 
            'soc_abbrev',
            'soc_whoart_code', 
            'soc_harts_code', 
            'soc_costart_sym',
            'soc_icd9_code', 
            'soc_icd9cm_code', 
            'soc_icd10_code', 
            'soc_jart_code'
        ]
    }

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    soc_code: Mapped[int] = mapped_column(Numeric(10,2))
    soc_name: Mapped[str] = mapped_column(String(100))
    soc_abbrev: Mapped[str] = mapped_column(String(5))

    soc_whoart_code: Mapped[Optional[str]] = mapped_column(String(7), comment='A partir de la versión 15.0 de MedDRA, estos campos no contienen datos.')
    soc_harts_code: Mapped[Optional[int]] = mapped_column(Numeric(10,2), comment='A partir de la versión 15.0 de MedDRA, estos campos no contienen datos.')
    soc_costart_sym: Mapped[Optional[str]] = mapped_column(String(21), comment='A partir de la versión 15.0 de MedDRA, estos campos no contienen datos.')
    soc_icd9_code: Mapped[Optional[str]] = mapped_column(String(8), comment='A partir de la versión 15.0 de MedDRA, estos campos no contienen datos.')
    soc_icd9cm_code: Mapped[Optional[str]] = mapped_column(String(8), comment='A partir de la versión 15.0 de MedDRA, estos campos no contienen datos.')
    soc_icd10_code: Mapped[Optional[str]] = mapped_column(String(8), comment='A partir de la versión 15.0 de MedDRA, estos campos no contienen datos.')
    soc_jart_code: Mapped[Optional[str]] = mapped_column(String(6), comment='A partir de la versión 15.0 de MedDRA, estos campos no contienen datos.')
    
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    language: Mapped[Optional[str]] = mapped_column(String(8))
    version: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(5, 2))

def get_model_columns(model_class) -> List[str]:
    """Extract column names from a model, excluding certain columns."""
    meddra_file_cols = model_class.__meddra_file_info__.get('_column_order', [])
    
    columns = []
    for name, _ in model_class.__annotations__.items():
        # Skip excluded columns and private attributes
        if name in EXCLUDED_COLUMNS or name.startswith('_'):
            continue
        
        # The model should have the same column names as the meddra_file_cols
        if name not in meddra_file_cols:
            raise ValueError(f"Column {name} not found in model {model_class.__name__}")
        
        columns.append(name)
    return columns

def generate_meddra_file_mappings():
    """
    Dynamically generate MedDRA file mappings from model class attributes.
    """
    mappings = {}
    
    for cls in Base.__subclasses__():
        if hasattr(cls, '__meddra_file_info__'):
            file_info = cls.__meddra_file_info__
            filename = file_info['filename']
            # Use file_columns if specified, otherwise get them from the model
            # if 'file_columns' in file_info:
            #     columns = file_info['file_columns']
            # else:

            columns = get_model_columns(cls)
            
            mappings[filename] = {
                'model': cls,
                'columns': columns
            }
    
    return mappings

if __name__ == "__main__":
    from config import DatabaseConfig
    from sqlalchemy import create_engine

    # Carga la configuración de la base de datos desde las variables de entorno
    db_config = DatabaseConfig.from_env()
    engine = create_engine(db_config.url)

    with engine.connect() as conn:
        conn.execute(text('CREATE SCHEMA IF NOT EXISTS meddra'))
        conn.commit()

    # Crea todas las tablas definidas en los modelos si no existen
    Base.metadata.drop_all(engine)  # Drop all tables first
    Base.metadata.create_all(engine)  # Recreate all tables