<?php
header("content-type:text/html;charset=utf-8");
/**
 * 	TestLink Open Source Project - http://testlink.sourceforge.net/
 *
 * 	@version 	$Id: listTestCases.php,v 1.60 2010/09/15 20:55:12 franciscom Exp $
 * 	@author 	Martin Havlat
 *
 * 	Generates tree menu with test specification.
 *   It builds the javascript tree that allows the user to choose testsuite or testcase.
 *
 *	@internal revision
 *
 *   20100628 - asimon - removal of constants from filter control class
 *   20100624 - asimon - CVS merge (experimental branch to HEAD)
 *   20100622 - asimon - huge refactorization for new tlTestCaseFilterControl class
 *   20100517 - asimon - BUGID 3301 and related - huge refactoring for first implementation
 *                       of filter panel class hierarchy to simplify/standardize
 *                       filter panel handling for test cases and requirements
 *   20100428 - asimon - BUGID 3301 and related issues - changed name or case
 *                       of some variables used in new common template,
 *                       added custom field filtering logic
 *	20091210 - franciscom - test case execution type filter
 *   20090308 - franciscom - added option Any in keywords filter
 *   20090210 - BUGID 2062 - franciscom -
 */
require_once('../../config.inc.php');
require_once("common.php");
require_once("treeMenu.inc.php");
require_once('../../third_party/codeplex/PHPExcel.php');

testlinkInitPage($db);

$templateCfg = templateConfiguration();
// new class for filter controlling/handling
$control = new tlTestCaseFilterControl($db, 'edit_mode');

$gui = initializeGui($db, $control);

$control->build_tree_menu($gui);
$_REQUEST = strings_stripSlashes($_REQUEST);

$do_export = isset($_REQUEST['doexport']) ? 1 : 0;
//获取主目录
$base_href = $_SESSION['basehref'];

if ($gui->childs && $do_export) {
  $project_name = null;
  $model_node = current($gui->childs); // 模块数据
  $model_id = intval($model_node['id']); // 一级模块ID
  $sql = "select NH.name as project_name from testsuites TSS join nodes_hierarchy NH  on  TSS.project_id=NH.id where TSS.id={$model_id}";
  $rs = $db->get_recordset($sql);

  if (count($rs)) {
    $project_name = $rs[0]['project_name'];  // 读取基线名称
  }
  $sp = "<br>";
  $basepath = './temp/';
  $user = $_SESSION['currentUser']->getDisplayName();
  $userpath = $basepath . $user . "/";    // /temp/admin/
  if (!file_exists($userpath)) {
    mkdir($userpath);
  }

  $fpath = $basepath . $user . "/testcases/"; // /temp/admin/testcases/
  if (is_null($project_name)) {
    $zipfilename = $basepath . $user . "/result.zip";
  } else {
    $zipfilename = $basepath . $user . "/" . str_replace("*", '', $project_name) . ".zip";  // /temp/admin/基线名称.zip
  }
  // $zipfilename=iconv("utf-8","gb2312//IGNORE",$zipfilename);
  $imgpath = $basepath . $user . "/images/";  // /temp/admin/images/

  // 清空文件：用例和图片
  deldir($imgpath);
  deldir($fpath);
  if (!file_exists($fpath)) {
    mkdir($fpath);
  }
  if (!file_exists($imgpath)) {
    mkdir($imgpath);
  }

  $priority_map = array('1' => '顶', '2' => '高', '3' => '中', '4' => '低', 1 => '顶', 2 => '高', 3 => '中', 4 => '低');
  $exectype_map = array('1' => '手动', '2' => '自动', '3' => '挂起', 1 => '手动', 2 => '自动', 3 => '挂起');

  $tcase_mgr = new testcase($db);
  $allfile = array();
  $pattern_tr = '/<tr.*?>(.*?)<\/tr>/s';
  $pattern_td = '/<td.*?>(.*?)<\/td>/s';
  //对Old] Old_Testlink的处理
  $indexaa = 1;
  foreach ($gui->childs as $key => $node) {
    if ($node['name'] == "Old] Old_Testlink" || $node['name'] == "Old]* Old_Testlink") {
      foreach ($node['childNodes'] as $old_node) {
        $gui->childs[] = $old_node;
        $indexaa += 1;
      }
      unset($gui->childs[$key]);
    }
  }

  foreach ($gui->childs as $node) {
    $model_name = $node['name'];  // 一级模块名
    $model_name = str_replace('/', '_', $model_name);
    $model_id = intval($node['id']); // 一级模块ID
    $filename = $fpath . $model_name . "_old.xls";

    $filename = str_replace('*', '', $filename);
    // $filename = iconv("utf-8", "gb2312//IGNORE", $filename);

    $auto_file_name = $fpath . $model_name . ".xls";
    $auto_file_name = str_replace('*', '', $auto_file_name);
    // $auto_file_name = iconv("utf-8", "gb2312//IGNORE", $auto_file_name);

    if (file_exists($filename)) {
      unlink($filename);
    }
    if (file_exists($auto_file_name)) {
      unlink($auto_file_name);
    }

    $objPHPExcel = null;
    $PHPExcelAuto = null;
    $MainWorkSheet = null;
    $index = 2;
    $dirindex = 2;
    $auto_index = 2;

    if (array_key_exists('childNodes', $node)) {
      foreach ($node['childNodes'] as $child_node) {
        $submodel_name = $child_node['name']; // 二级模块名
        $submodel_id = intval($child_node['id']); // 二级模块ID
        $summodel_index = substr($submodel_name, 0, strpos($submodel_name, ']')); // LocWiFi_Prefer_5G.Int
        $bauto = getmodeltype($db, $submodel_id);

        /* 
        Array
        (
            [6070345] => WEB_Sec.Sec.0] 模块环境设置
            [6070496] => WEB_Sec.Sec.C] 模块环境清理
        )
        */
        if (is_null($PHPExcelAuto) && $bauto) {
          $PHPExcelAuto = new PHPExcel();
          $PHPExcelAuto->setActiveSheetIndex(0);
          $PHPExcelAuto->getDefaultStyle()->getFont()->setName('宋体');
          $PHPExcelAuto->getDefaultStyle()->getFont()->setSize(9);

          $list_sheep = $PHPExcelAuto->getActiveSheet();
          $list_sheep->setTitle('目录');
          $title = array('A' => array(50, '用例名称'), 'B' => array(20, '测试结果'), 'C' => array(30, '摘要'), 'D' => array(20, 'bugfree'));
          foreach ($title as $k => $v) {
            $list_sheep->setCellValue($k . "1", $v[1]);
            $list_sheep->getColumnDimension($k)->setWidth($v[0]);
          }
          $list_index = 2;
          $case_sheep = new PHPExcel_Worksheet($PHPExcelAuto, 'testcase'); //创建一个工作表
          $PHPExcelAuto->addSheet($case_sheep); //插入工作表


          $case_sheep->getDefaultRowDimension()->setRowHeight(-1);
          $title = array(
            'A' => array(5, 'ID'), 'B' => array(20, '测试项'), 'C' => array(20, '摘要'), 'D' => array(40, '关键动作(重点是"做什么"，而不是"怎么做")'),
            'E' => array(30, '测试点'), 'F' => array(10, 'Pri'), 'G' => array(10, '方式'), 'H' => array(10, '耗时(手动=>自动后)')
          );
          foreach ($title as $k => $v) {
            $case_sheep->setCellValue($k . "1", $v[1]);
            $case_sheep->getColumnDimension($k)->setWidth($v[0]);
          }
          $case_sheep->mergeCells('I1:L1');
          $case_sheep->setCellValue('I1', '数据源');
          $TopoSheet = new PHPExcel_Worksheet($PHPExcelAuto, '拓扑图'); //创建一个工作表
          $PHPExcelAuto->addSheet($TopoSheet); //插入工作表
        }
        if ($bauto) {
          list($first_id, $last_id) = array_keys($bauto);
          $before = $tcase_mgr->get_by_id(intval($first_id), 0, null, array('ghoststeps' => false));
          $before_name = $before[0]['name'];
          $steps_before = $before[0]['steps'];
          $steps_str = '';
          foreach ($steps_before as $step) {
            $steps_str .= $step['actions'] . "\n";
          }
          $steps_str = strip_tags($steps_str);

          // 加入环境模块设置
          // $TopoSheet

          // preg_match_all('/src=\"data:image\/(.*?);base64,(.*?)\"/i',$precondition,$match);
          // if ($match) {
          // $imgfilename=$imgpath.$case_id.'.'.$match[1][0];
          // file_put_contents($imgfilename, base64_decode($match[2][0]));
          // 从预置条件中移除图片信息
          // $precondition=preg_replace('/<img.*\/>/','', $precondition);
          // }
          $topoindex = 1;
          $before_preconditions = $before[0]['preconditions'];
          if (strpos($before_preconditions, 'img:')) {
            $strs = explode(',', $before_preconditions);
            $img_width = 300;
            $img_Height = 240;
            $pic_info = array();
            $case_id = $first_id;
            foreach ($strs as $str) {
              $info_array = explode(':', $str);
              switch ($info_array[0]) {
                case 'name':
                  $pic_info['name'] = $info_array[1];
                  break;
                case 'Width':
                  $pic_info['Width'] = $info_array[1];
                  break;
                case 'Height':
                  $pic_info['Height'] = $info_array[1];
                  break;
                case 'img':
                  $pic_info['img'] = $info_array[1];
                  $imgfilename = $imgpath . $case_id . $topoindex . ".jpg";
                  file_put_contents($imgfilename, base64_decode($pic_info['img']));
                  $objDrawing = new PHPExcel_Worksheet_Drawing();
                  $objDrawing->setName($pic_info['name']);
                  $objDrawing->setDescription($pic_info['name']);
                  $objDrawing->setPath($imgfilename);
                  $objDrawing->setHeight($pic_info['Height']);
                  $objDrawing->setWidth($pic_info['Width']);
                  $objDrawing->setCoordinates('A' . ($topoindex + 1));
                  $objDrawing->setWorksheet($TopoSheet);
                  $TopoSheet->getRowDimension($topoindex + 1)->setRowHeight($pic_info['Height']);
                  $TopoSheet->setCellValue('A' . $topoindex, $bauto[$first_id]);
                  $topoindex += 1;
                  break;
              }
            }
          }

          if (preg_match_all('/src=\"data:image\/(.*?);base64,(.*?)\"/i/s', $before_preconditions, $match)) {
            $imgfilename = $imgpath . $case_id . '.' . $match[1][0];
            file_put_contents($imgfilename, base64_decode($match[2][0]));
            $objDrawing = new PHPExcel_Worksheet_Drawing();
            $objDrawing->setName('auto');
            $objDrawing->setDescription('auto');
            $objDrawing->setPath($imgfilename);
            $objDrawing->setHeight(240);
            $objDrawing->setWidth(300);
            $objDrawing->setCoordinates('A' . ($topoindex + 1));
            $objDrawing->setWorksheet($TopoSheet);
            $TopoSheet->getRowDimension($topoindex + 1)->setRowHeight(240);
            $TopoSheet->setCellValue('A' . $topoindex, $bauto[$first_id]);
            $topoindex += 1;
          }
          
          $case_sheep->setCellValue('B' . $auto_index, $bauto[$first_id]);
          $case_sheep->getStyle('B' . $auto_index)->getAlignment()->setVertical(PHPExcel_Style_Alignment::VERTICAL_CENTER);
          $case_sheep->getStyle('B' . $auto_index)->getAlignment()->setWrapText(true);
          $case_sheep->getStyle('D' . $auto_index)->getAlignment()->setWrapText(true);
          $case_sheep->setCellValue('D' . $auto_index, $steps_str);
          $case_sheep->setCellValue('E' . $auto_index, '// 0) 模块环境设置');
          $auto_index += 2;
          $case_count = 0;
          if (array_key_exists('childNodes', $child_node)) {
            foreach ($child_node['childNodes'] as $item_node) {
              
              $item_name = $item_node['name'];
              
              $item_index = substr($item_name, 0, strpos($item_name, ']'));
              $item_id = intval($item_node['id']);
              if ($item_name == $bauto[$first_id] || $item_name == $bauto[$last_id]) {
                // 排除环境模块设置和清理，不管是否筛选出来，必须前期处理
                continue;
              }
 
              $item_prefer = substr($item_name, 0, strpos($item_name, ']'));
 
              $sum_id = getsuminfo($db, $item_prefer . '.Sum]', $item_id);

              if (!$sum_id) {
                $sum_id = getsuminfo($db, $item_prefer . '.Sum]* ', $item_id);
              }

              if (!$sum_id) {
                continue;
              }
              $sum_info = $tcase_mgr->get_by_id(intval($sum_id), 0, null, array('ghoststeps' => false));
              $before_step = '';
              $run_step = '';
              $after_step = '';
              if ($sum_info) {
                $steps = $sum_info[0]['steps'];
                $steps_str = '';
                foreach ($steps as $step) {
                  $steps_str .= $step['actions'] . "\n";
                }
                $steps_str = strip_tags($steps_str);
                if (preg_match('/\/\/BeforItem;?(.*)\/\/Before;?/s', $steps_str, $match)) {
                  $before_step = $match[1];
                }
                if (preg_match('/\/\/Before;?(.*)\/\/AfterItem;?/s', $steps_str, $match)) {
                  $run_step = '//Before' . $match[1];
                }
                if (preg_match('/\/\/AfterItem;?(.*)/s', $steps_str, $match)) {
                  $after_step = $match[1];
                }
              }

              if (array_key_exists('childNodes', $item_node)) {
                $case_count = count($item_node['childNodes']);
                foreach ($item_node['childNodes'] as $case_node) {
                  $case_id = intval($case_node['id']);
                  if ($case_id == $sum_id) {
                    $case_count -= 1;
                  }
                }
                // echo "case_count:".$case_count."<br>";
                $endline = $auto_index + $case_count + 1;
                $case_sheep->mergeCells('A' . $auto_index . ":A" . $endline);
                $case_sheep->mergeCells('B' . $auto_index . ":B" . $endline);
                $case_sheep->mergeCells('C' . $auto_index . ":C" . $endline);
                if ($case_count > 1) {
                  $case_sheep->mergeCells('D' . ($auto_index + 1) . ":D" . ($endline - 1));
                }
                $case_sheep->getStyle('B' . $auto_index)->getAlignment()->setVertical(PHPExcel_Style_Alignment::VERTICAL_CENTER);
                $case_sheep->getStyle('B' . $auto_index)->getAlignment()->setWrapText(true);
                $case_sheep->setCellValue('B' . $auto_index, $item_name);
                $case_sheep->getStyle('D' . $auto_index)->getAlignment()->setWrapText(true);
                $case_sheep->getStyle('D' . $auto_index)->getAlignment()->setShrinkToFit(true);
                $case_sheep->getStyle('D' . ($auto_index + 1))->getAlignment()->setWrapText(true);
                $case_sheep->getStyle('D' . ($auto_index + 1))->getAlignment()->setShrinkToFit(true);
                $case_sheep->getStyle('D' . $endline)->getAlignment()->setWrapText(true);
                $case_sheep->getStyle('D' . $endline)->getAlignment()->setShrinkToFit(true);
                $case_sheep->setCellValue('D' . $auto_index, $before_step);
                $case_sheep->setCellValue('D' . ($auto_index + 1), $run_step);
                $case_sheep->setCellValue('D' . $endline, $after_step);

                // reset($item_node['childNodes']);
                // $firstcase=current($item_node['childNodes']);
                // if (intval($firstcase['id'])==$sum_id) {
                // $firstcase=next($item_node['childNodes']);
                // }

                // 表头信息处理完毕
                $dotitle = false;
                foreach ($item_node['childNodes'] as $case_node) {
                  $case_id = intval($case_node['id']);
                  if ($case_id == $sum_id) {
                    continue;
                  } elseif (!$dotitle) {
                    // / 拆分获取表格表头信息
                    $case_info = $tcase_mgr->get_by_id($case_node['id'], 0, null, array('ghoststeps' => false));
                    $summary = $case_info[0]['summary'];
                    $titles = array();
                    $table = preg_replace("/([\r\n\t]+)/", '', $summary);
                    if (preg_match_all($pattern_tr, $table, $matches)) {
                      $title_tr = $matches[1][0];
                      if (preg_match_all($pattern_td, $title_tr, $matches_title)) {
                        $titles = $matches_title[1];
                      }
                    }

                    // $begincol = ord('I');
                    $colidx = ['I' => 8];
                    $index_col = 0;

                    foreach ($titles as $title) {
                      $colname = columnNameConvert($colidx['I'] + $index_col);
                      $case_sheep->setCellValue($colname . $auto_index, $title);
                      $case_sheep->getColumnDimension($colname)->setWidth(15);
                      $index_col += 1;
                    }
                    $auto_index += 1;
                    $dotitle = true;
                  }

                  $case_name = $case_node['name'];
                  $case_name = str_replace($item_index . ".", '', $case_name);
                  $case_id = intval($case_node['id']);
                  // file_put_contents("C:/xampp/htdocs/testlink/logs/case_name.txt",var_export($case_name,true),FILE_APPEND);
                  $case_info = $tcase_mgr->get_by_id($case_id, 0, null, array('ghoststeps' => false));
                  // file_put_contents("C:/xampp/htdocs/testlink/logs/case_info.txt",var_export($case_info,true),FILE_APPEND);
                  $case_sheep->setCellValue('E' . $auto_index, $case_name);
                  //开始插入目录
                  $list_sheep->setCellValue('A' . $list_index, $case_node['name']);
                  //超链接
                  $list_sheep->getCell('A' . $list_index)->getHyperlink()->setUrl('sheet://testcase!' . 'E' . $auto_index);
                  $case_sheep->getCell('E' . $auto_index)->getHyperlink()->setUrl('sheet://目录!' . 'A' . $list_index);
                  //选项
                  $objValidation = $list_sheep->getCell('B' . $list_index)->getDataValidation(); //这一句为要设置数据有效性的单元格
                  $objValidation->setType(PHPExcel_Cell_DataValidation::TYPE_LIST)
                    ->setErrorStyle(PHPExcel_Cell_DataValidation::STYLE_INFORMATION)
                    ->setAllowBlank(false)
                    ->setShowInputMessage(true)
                    ->setShowErrorMessage(true)
                    ->setShowDropDown(true)
                    ->setErrorTitle('输入的值有误')
                    ->setError('您输入的值不在下拉框列表内.')
                    ->setPromptTitle('测试结果')
                    ->setFormula1('"成功,失败,锁定"');
                  $list_index += 1;

                  $case_sheep->getStyle('E' . $auto_index)->getAlignment()->setWrapText(true);
                  $case_sheep->setCellValue('F' . $auto_index, $priority_map[$case_info[0]['importance']]);
                  $case_sheep->setCellValue('G' . $auto_index, $exectype_map[$case_info[0]['execution_type']]);
                  if (!$case_info[0]['estimated_exec_duration']) {
                    $case_info[0]['estimated_exec_duration'] = 5;
                  }
                  $case_sheep->setCellValue('H' . $auto_index, $case_info[0]['estimated_exec_duration'] . '=>' . $case_info[0]['auto_exec_duration']);
                  $summary = $case_info[0]['summary'];
                  // 开始处理数据源数据
                  $titles = array();
                  $table = preg_replace("/([\r\n\t]+)/", '', $summary);
                  if (preg_match_all($pattern_tr, $table, $matches)) {
                    $title_tr = $matches[1][1];
                    if (preg_match_all($pattern_td, $title_tr, $matches_title)) {
                      $titles = $matches_title[1];
                    }
                  }
                  $index_col = 0;

                  foreach ($titles as $title) {
                    $colname = columnNameConvert($colidx['I'] + $index_col);
                    // $cellpos = chr($begincol + $index_col) . $auto_index;
                    $cellpos = $colname . $auto_index;
                    $case_sheep->setCellValueExplicit($cellpos, $title, PHPExcel_Cell_DataType::TYPE_STRING);
                    $case_sheep->getStyle($cellpos)->getAlignment()->setWrapText(true);
                    $case_sheep->getStyle($cellpos)->getFont()->getColor()->setARGB(PHPExcel_Style_Color::COLOR_DARKBLUE);

                    $index_col += 1;
                  }
                  // 数据源信息处理完毕
                  $auto_index += 1;
                }
                $auto_index = $endline + 1;
              }
            }
            $auto_index += 1;
            $case_sheep->setCellValue('B' . $auto_index, $bauto[$last_id]);
            $case_sheep->setCellValue('E' . $auto_index, 'C) 模块环境清理');
            $case_sheep->getStyle('B' . $auto_index)->getAlignment()->setWrapText(true);
            $case_sheep->getStyle('E' . $auto_index)->getAlignment()->setWrapText(true);
            // C) 模块环境清理
            $auto_index += 2;
          }
        }


        if (is_null($objPHPExcel) && !$bauto) {  // testlink老模板
          //设定表头
          $objPHPExcel = new PHPExcel();
          $objPHPExcel->setActiveSheetIndex(0);
          $objPHPExcel->getDefaultStyle()->getFont()->setName('宋体');
          $objPHPExcel->getDefaultStyle()->getFont()->setSize(9);

          /* 目录工作表 */
          $this_sheep = $objPHPExcel->getActiveSheet();  // 目录表
          $this_sheep->setTitle('目录');

          $title = array('A' => array(50, '用例名称'), 'B' => array(20, '测试结果'), 'C' => array(30, '摘要'), 'D' => array(20, 'bugfree'));
          foreach ($title as $k => $v) {
            $this_sheep->setCellValue($k . "1", $v[1]);
            $this_sheep->getColumnDimension($k)->setWidth($v[0]);
          }

          /* 用例工作表 */
          $MainWorkSheet = new PHPExcel_Worksheet($objPHPExcel, 'testcase'); //创建一个工作表
          $objPHPExcel->addSheet($MainWorkSheet); //插入工作表
          $title = array(
            'A' => array(20, '一级模块名称'), 'B' => array(20, '二级模块'), 'C' => array(30, '测试项名称'), 'D' => array(20, '用例名称'),
            'E' => array(30, '摘要'), 'F' => array(30, '预置条件'), 'G' => array(50, '测试步骤'), 'H' => array(10, '优先级'), 'I' => array(10, '手工执行时间'), 'J' => array(50, '拓扑图')
          );
          foreach ($title as $k => $v) {
            $MainWorkSheet->setCellValue($k . "1", $v[1]);
            $MainWorkSheet->getColumnDimension($k)->setWidth($v[0]);
          }
          $MainWorkSheet->setCellValue('A' . $index, $model_name);
          $model_prefer = substr($model_name, 0, strpos($model_name, ']')); // 一级模块名
          $index += 1;
        }

        if (!$bauto) {
          $new_submodel_name = str_replace($model_prefer . ".", '', $submodel_name); // Int]* 集成测试

          $submodel_prefer = substr($submodel_name, 0, strpos($submodel_name, ']')); // LocWiFi_Prefer_5G.Int
          $MainWorkSheet->setCellValue('B' . $index, $new_submodel_name);
          $index += 1;
          if (array_key_exists('childNodes', $child_node)) {
            foreach ($child_node['childNodes'] as $item_node) {
              $item_name = $item_node['name']; // 三级模块名 LocWiFi_Prefer_5G.Int.1)* 无线客户端使用2.4G连接,被拒绝后还继续2.4G连接
              $item_name = str_replace('*','',$item_name);
              $new_item_name = str_replace($submodel_prefer . ".", '', $item_name); // 1)* 无线客户端使用2.4G连接,被拒绝后还继续2.4G连接使用2.4G连接,被拒绝后还继续2.4G连接
              $new_item_name = str_replace(')',']',$new_item_name);
              $item_name_prefer = substr($item_name, 0, strpos($item_name, ']')); // LocWiFi_Prefer_5G.Int.1
              $MainWorkSheet->setCellValue('C' . $index, $new_item_name);
              $index += 1;
              if (array_key_exists('childNodes', $item_node)) {
                foreach ($item_node['childNodes'] as $case_node) {
                  $case_name = $case_node['name'];
                  $case_id = intval($case_node['id']);
                  $new_case_name = str_replace($item_name_prefer . ".", '', $case_name);
                  $MainWorkSheet->setCellValue('D' . $index, $new_case_name);
                  $this_sheep->setCellValue('A' . $dirindex, $case_name);
                  $this_sheep->getCell('A' . $dirindex)->getHyperlink()->setUrl('sheet://testcase!' . 'D' . $index);
                  $objValidation = $this_sheep->getCell('B' . $dirindex)->getDataValidation(); //这一句为要设置数据有效性的单元格
                  $objValidation->setType(PHPExcel_Cell_DataValidation::TYPE_LIST)
                    ->setErrorStyle(PHPExcel_Cell_DataValidation::STYLE_INFORMATION)
                    ->setAllowBlank(false)
                    ->setShowInputMessage(true)
                    ->setShowErrorMessage(true)
                    ->setShowDropDown(true)
                    ->setErrorTitle('输入的值有误')
                    ->setError('您输入的值不在下拉框列表内.')
                    ->setPromptTitle('测试结果')
                    ->setFormula1('"成功,失败,锁定"');
                  #其他步骤等参数
                  $case_info = $tcase_mgr->get_by_id($case_id, 0, null, array('ghoststeps' => false));
                  if (!is_null($case_info)) {
                    $imgfilename = null;
                    $summary = $case_info[0]['summary'];
                    $importance = $case_info[0]['importance'];
                    $precondition = $case_info[0]['preconditions'];

                    // $summary = htmlspecialchars_replace($summary);
                    // $precondition = htmlspecialchars_replace($precondition);
                    preg_match_all('/src=\"data:image\/(.*?);base64,(.*?)\"/i', $precondition, $match1);
                    preg_match_all('/src=data:image\/(.*?);base64,(.*?)\>/i', $precondition, $match2);
                    $match = '';
                    if (!empty($match1[0])) $match = $match1;
                    if (!empty($match2[0])) $match = $match2;
                    if ($match) {
                      $imgfilename = $imgpath . $case_id . '.' . $match[1][0];
                      file_put_contents($imgfilename, base64_decode($match[2][0]));
                      // 从预置条件中移除图片信息
                      $precondition = preg_replace('/<img.*\/>/', '', $precondition);
                    }
                    $estimated_exec_duration = $case_info[0]['estimated_exec_duration'];
                    $steps = $case_info[0]['steps'];
                    // var_dump($steps);
                    // break;
                    $steps_str = '';
                    foreach ($steps as $step) {
                      $step_num = '';
                      if ((preg_match('/^\d+>/i', $step['actions']) == 0) && (substr($step['actions'], 0, 2) != "//")) {
                        // echo preg_match('/^\d+>/i',$step['actions'])." :|".$step['actions']."substr:".substr($step['actions'],0,2)."<br>";
                        $steps_str .= $step['step_number'] . ">";
                      }
                      if (trim($step['expected_results'])) {
                        $steps_str .= $step_num . $step['actions'] . '【预期】' . $step['expected_results'] . "\n";
                      } else {
                        $steps_str .= $step_num . $step['actions'] . "\n";
                      }
                    }

                    $summary = strip_tags($summary);
                    $precondition = strip_tags($precondition);
                    $steps_str = strip_tags($steps_str);
                    // <p>
                    // 开始添加用例其余部分
                    $MainWorkSheet->getStyle('E' . $index)->getAlignment()->setWrapText(true);
                    $MainWorkSheet->getStyle('F' . $index)->getAlignment()->setWrapText(true);
                    $MainWorkSheet->getStyle('G' . $index)->getAlignment()->setWrapText(true);
                    $MainWorkSheet->getStyle('H' . $index)->getAlignment()->setWrapText(true);
                    $MainWorkSheet->getStyle('I' . $index)->getAlignment()->setWrapText(true);
                    $MainWorkSheet->setCellValue('E' . $index, $summary);
                    $MainWorkSheet->setCellValue('F' . $index, $precondition);
                    $MainWorkSheet->setCellValue('G' . $index, $steps_str);
                    $MainWorkSheet->setCellValue('H' . $index, $priority_map[$importance]);
                    $MainWorkSheet->setCellValue('I' . $index, $estimated_exec_duration);
                    if ($imgfilename) {
                      $MainWorkSheet->getRowDimension($index)->setRowHeight(100);
                      $objDrawing = new PHPExcel_Worksheet_Drawing();
                      // echo "\n found picture: ".$pic_path."\n";
                      $objDrawing->setPath($imgfilename);
                      /*设置图片高度*/
                      $objDrawing->setHeight(100);
                      /*设置图片要插入的单元格*/
                      $objDrawing->setCoordinates("J" . strval($index));
                      /*设置图片所在单元格的格式*/
                      $objDrawing->setOffsetX(0);
                      $objDrawing->setRotation(0);
                      $objDrawing->getShadow()->setVisible(true);
                      $objDrawing->getShadow()->setDirection(0);
                      $objDrawing->setWorksheet($MainWorkSheet);
                    }
                  }
                  $index += 1;
                  $dirindex += 1;
                }
              } elseif ($item_node['node_table']=='testcases') {
                // a($item_node);
                $case_name = $item_name;
                $case_id = intval($item_node['id']);
                // $new_case_name = str_replace($item_name_prefer . ".", '', $case_name);
                $new_case_name = str_replace($submodel_prefer . ".", '', $case_name);
                // $new_case_name = $new_item_name;
                $MainWorkSheet->setCellValue('D' . $index, $new_case_name);
                $this_sheep->setCellValue('A' . $dirindex, $case_name);
                $this_sheep->getCell('A' . $dirindex)->getHyperlink()->setUrl('sheet://testcase!' . 'D' . $index);

                $objValidation = $this_sheep->getCell('B' . $dirindex)->getDataValidation(); //这一句为要设置数据有效性的单元格
                $objValidation->setType(PHPExcel_Cell_DataValidation::TYPE_LIST)
                  ->setErrorStyle(PHPExcel_Cell_DataValidation::STYLE_INFORMATION)
                  ->setAllowBlank(false)
                  ->setShowInputMessage(true)
                  ->setShowErrorMessage(true)
                  ->setShowDropDown(true)
                  ->setErrorTitle('输入的值有误')
                  ->setError('您输入的值不在下拉框列表内.')
                  ->setPromptTitle('测试结果')
                  ->setFormula1('"成功,失败,锁定"');
                #其他步骤等参数
                $case_info = $tcase_mgr->get_by_id($case_id, 0, null, array('ghoststeps' => false));
                if (!is_null($case_info)) {
                  $imgfilename = null;
                  $summary = $case_info[0]['summary'];
                  $importance = $case_info[0]['importance'];
                  $precondition = $case_info[0]['preconditions'];
                  // preg_match_all('/src=\"data:image\/(.*?);base64,(.*?)\"/i', $precondition, $match);
                  preg_match_all('/src=\"data:image\/(.*?);base64,(.*?)\"/i', $precondition, $match1);
                  preg_match_all('/src=data:image\/(.*?);base64,(.*?)\>/i', $precondition, $match2);
                  $match = '';
                  if (!empty($match1[0])) $match = $match1;
                  if (!empty($match2[0])) $match = $match2;

                  if ($match) {
                    $imgfilename = $imgpath . $case_id . '.' . $match[1][0];
                    file_put_contents($imgfilename, base64_decode($match[2][0]));
                    // 从预置条件中移除图片信息
                    $precondition = preg_replace('/<img.*\/>/', '', $precondition);
                  }
                  $estimated_exec_duration = $case_info[0]['estimated_exec_duration'];
                  $steps = $case_info[0]['steps'];
                  // var_dump($steps);
                  // break;
                  $steps_str = '';
                  foreach ($steps as $step) {
                    $step_num = '';
                    if ((preg_match('/^\d+>/i', $step['actions']) == 0) && (substr($step['actions'], 0, 2) != "//")) {
                      // echo preg_match('/^\d+>/i',$step['actions'])." :|".$step['actions']."substr:".substr($step['actions'],0,2)."<br>";
                      $steps_str .= $step['step_number'] . ">";
                    }
                    if (trim($step['expected_results'])) {
                      $steps_str .= $step_num . $step['actions'] . '【预期】' . $step['expected_results'] . "\n";
                    } else {
                      $steps_str .= $step_num . $step['actions'] . "\n";
                    }
                  }

                  $summary = strip_tags($summary);
                  $precondition = strip_tags($precondition);
                  $steps_str = strip_tags($steps_str);
                  // <p>
                  // 开始添加用例其余部分
                  $summary = str_replace('&nbsp;',' ',$summary);
                  $steps_str = str_replace('&nbsp;',' ',$steps_str);
                  $MainWorkSheet->getStyle('E' . $index)->getAlignment()->setWrapText(true);
                  $MainWorkSheet->getStyle('F' . $index)->getAlignment()->setWrapText(true);
                  $MainWorkSheet->getStyle('G' . $index)->getAlignment()->setWrapText(true);
                  $MainWorkSheet->getStyle('H' . $index)->getAlignment()->setWrapText(true);
                  $MainWorkSheet->getStyle('I' . $index)->getAlignment()->setWrapText(true);
                  $MainWorkSheet->setCellValue('E' . $index, $summary);
                  $MainWorkSheet->setCellValue('F' . $index, $precondition);
                  $MainWorkSheet->setCellValue('G' . $index, $steps_str);
                  $MainWorkSheet->setCellValue('H' . $index, $priority_map[$importance]);
                  $MainWorkSheet->setCellValue('I' . $index, $estimated_exec_duration);
                  if ($imgfilename) {
                    $MainWorkSheet->getRowDimension($index)->setRowHeight(100);
                    $objDrawing = new PHPExcel_Worksheet_Drawing();
                    // echo "\n found picture: ".$pic_path."\n";
                    $objDrawing->setPath($imgfilename);
                    /*设置图片高度*/
                    $objDrawing->setHeight(100);
                    /*设置图片要插入的单元格*/
                    $objDrawing->setCoordinates("J" . strval($index));
                    /*设置图片所在单元格的格式*/
                    $objDrawing->setOffsetX(0);
                    $objDrawing->setRotation(0);
                    $objDrawing->getShadow()->setVisible(true);
                    $objDrawing->getShadow()->setDirection(0);
                    $objDrawing->setWorksheet($MainWorkSheet);
                  }
                }
                $index += 1;
                $dirindex += 1;
              }
            }
          } elseif ($child_node['node_table']=='testcases') {
            /* 只有一级模块：设置二级模块名、三级模块名为标题*/
            $new_submodel_name = str_replace('*','',$new_submodel_name);
            $new_item_name = $new_submodel_name;

            if (preg_match('/\)/', $new_item_name, $matches)) {
              $new_item_name = str_replace(')',']',$new_item_name);
            }

            $MainWorkSheet->setCellValue('C' . $index, $new_item_name);

            // a($item_node);
            $submodel_name = str_replace('*','',$submodel_name);
            $case_name = $submodel_name;
            $case_id = intval($child_node['id']);
            $new_case_name = $new_submodel_name;
            // if (!preg_match('/\)/', $new_case_name, $matches)) {
            //   $new_case_name = ') ' . $new_case_name;
            // }
            $index += 1;
            $MainWorkSheet->setCellValue('D' . $index, $new_case_name);
            $this_sheep->setCellValue('A' . $dirindex, $case_name);
            $this_sheep->getCell('A' . $dirindex)->getHyperlink()->setUrl('sheet://testcase!' . 'D' . $index);

            $objValidation = $this_sheep->getCell('B' . $dirindex)->getDataValidation(); //这一句为要设置数据有效性的单元格
            $objValidation->setType(PHPExcel_Cell_DataValidation::TYPE_LIST)
              ->setErrorStyle(PHPExcel_Cell_DataValidation::STYLE_INFORMATION)
              ->setAllowBlank(false)
              ->setShowInputMessage(true)
              ->setShowErrorMessage(true)
              ->setShowDropDown(true)
              ->setErrorTitle('输入的值有误')
              ->setError('您输入的值不在下拉框列表内.')
              ->setPromptTitle('测试结果')
              ->setFormula1('"成功,失败,锁定"');
            #其他步骤等参数
            $case_info = $tcase_mgr->get_by_id($case_id, 0, null, array('ghoststeps' => false));
            if (!is_null($case_info)) {
              $imgfilename = null;
              $summary = $case_info[0]['summary'];
              $importance = $case_info[0]['importance'];
              $precondition = $case_info[0]['preconditions'];

              // preg_match_all('/src=\"data:image\/(.*?);base64,(.*?)\"/i', $precondition, $match);
              preg_match_all('/src=\"data:image\/(.*?);base64,(.*?)\"/i', $precondition, $match1);
              preg_match_all('/src=data:image\/(.*?);base64,(.*?)\>/i', $precondition, $match2);
              $match = '';
              if (!empty($match1[0])) $match = $match1;
              if (!empty($match2[0])) $match = $match2;
              
              if ($match) {
                $imgfilename = $imgpath . $case_id . '.' . $match[1][0];
                file_put_contents($imgfilename, base64_decode($match[2][0]));
                // 从预置条件中移除图片信息
                $precondition = preg_replace('/<img.*\/>/', '', $precondition);
              }
              $estimated_exec_duration = $case_info[0]['estimated_exec_duration'];
              $steps = $case_info[0]['steps'];
              // var_dump($steps);
              // break;
              $steps_str = '';
              foreach ($steps as $step) {
                $step_num = '';
                if ((preg_match('/^\d+>/i', $step['actions']) == 0) && (substr($step['actions'], 0, 2) != "//")) {
                  // echo preg_match('/^\d+>/i',$step['actions'])." :|".$step['actions']."substr:".substr($step['actions'],0,2)."<br>";
                  $steps_str .= $step['step_number'] . ">";
                }
                if (trim($step['expected_results'])) {
                  $steps_str .= $step_num . $step['actions'] . '【预期】' . $step['expected_results'] . "\n";
                } else {
                  $steps_str .= $step_num . $step['actions'] . "\n";
                }
              }

              $summary = strip_tags($summary);
              $precondition = strip_tags($precondition);
              $steps_str = strip_tags($steps_str);
              // <p>
              // 开始添加用例其余部分
              // $summary = htmlspecialchars_decode($summary);
              // $steps_str = htmlspecialchars_decode($steps_str);
              $summary = str_replace('&nbsp;',' ',$summary);
              $steps_str = str_replace('&nbsp;',' ',$steps_str);
              $MainWorkSheet->getStyle('E' . $index)->getAlignment()->setWrapText(true);
              $MainWorkSheet->getStyle('F' . $index)->getAlignment()->setWrapText(true);
              $MainWorkSheet->getStyle('G' . $index)->getAlignment()->setWrapText(true);
              $MainWorkSheet->getStyle('H' . $index)->getAlignment()->setWrapText(true);
              $MainWorkSheet->getStyle('I' . $index)->getAlignment()->setWrapText(true);
              $MainWorkSheet->setCellValue('E' . $index, $summary);
              $MainWorkSheet->setCellValue('F' . $index, $precondition);
              $MainWorkSheet->setCellValue('G' . $index, $steps_str);
              $MainWorkSheet->setCellValue('H' . $index, $priority_map[$importance]);
              $MainWorkSheet->setCellValue('I' . $index, $estimated_exec_duration);
              if ($imgfilename) {
                $MainWorkSheet->getRowDimension($index)->setRowHeight(100);
                $objDrawing = new PHPExcel_Worksheet_Drawing();
                // echo "\n found picture: ".$pic_path."\n";
                $objDrawing->setPath($imgfilename);
                /*设置图片高度*/
                $objDrawing->setHeight(100);
                /*设置图片要插入的单元格*/
                $objDrawing->setCoordinates("J" . strval($index));
                /*设置图片所在单元格的格式*/
                $objDrawing->setOffsetX(0);
                $objDrawing->setRotation(0);
                $objDrawing->getShadow()->setVisible(true);
                $objDrawing->getShadow()->setDirection(0);
                $objDrawing->setWorksheet($MainWorkSheet);
              }
            }
            $index += 1;
            $dirindex += 1;
          }
        }
      }
    }

    if (!is_null($objPHPExcel)) {
      $objWriter = PHPExcel_IOFactory::createWriter($objPHPExcel, 'Excel5');
      $objWriter->save($filename);
      $allfile[] = $filename;
      unset($objPHPExcel);
      $objPHPExcel = null;
    }

    if (!is_null($PHPExcelAuto)) {
      $objWriter = PHPExcel_IOFactory::createWriter($PHPExcelAuto, 'Excel5');
      $objWriter->save($auto_file_name);
      $allfile[] = $auto_file_name;
      unset($PHPExcelAuto);
      $PHPExcelAuto = null;
    }
  }
  if (count($allfile)) {
    zipfile($allfile, $zipfilename);
    $gui->downloadlink = $base_href . "lib/testcases/" . $zipfilename;
    // echo $gui->downloadlink;
  }
}

$smarty = new TLSmarty();
$smarty->assign('gui', $gui);
$smarty->assign('control', $control);
$smarty->assign('args', $control->get_argument_string());
$smarty->assign('menuUrl', $gui->menuUrl);

$smarty->display($templateCfg->template_dir . 'tcTree.tpl');

function zipfile($filearray, $filename)
{

  $zip = new ZipArchive();
  $ow = 1;
  // $filename=iconv("utf-8","gb2312//IGNORE",$filename);
  if ($zip->open($filename, ZIPARCHIVE::OVERWRITE | ZIPARCHIVE::CREATE) === TRUE) {
    for ($i = 0; $i < count($filearray); $i++) {
      $attachfile = $filearray[$i];
      $attachfilenames = explode('/', $attachfile);
      $attachfilename = end($attachfilenames);
      $attachfilename = iconv("utf-8","gb2312//IGNORE",$attachfilename);
      $zip->addfile($attachfile, $attachfilename);
      // $zip->addfile($attachfile, basename($attachfile));
    }
    $zip->close();
  }
}
function getsuminfo($dbobj, $node_name, $parent_id)
{
  $new_node_name = $node_name . "*";
  $sql = "select id from  nodes_hierarchy where parent_id={$parent_id} and (trim(replace(name,'\\n',''))='{$node_name}' or trim(replace(name,'\\n',''))='{$new_node_name}')";
  $rs = $dbobj->get_recordset($sql);
  if (count($rs)) {
    return $rs[0]['id'];
  } else {
    return null;
  }
}
function deldir($dir)
{
  //先删除目录下的文件：
  $dh = opendir($dir);
  while ($file = readdir($dh)) {
    if ($file != "." && $file != "..") {
      $fullpath = $dir . "/" . $file;
      if (!is_dir($fullpath)) {
        unlink($fullpath);
      } else {
        deldir($fullpath);
      }
    }
  }
  closedir($dh);
  // 删除当前文件夹：
  // if(rmdir($dir)) {
  // return true;
  // } else {
  // return false;
  // }
}
function getmodeltype($dbobj, $id)
{
  $first_id = 0;
  $last_id = 0;
  $sql = "select NHC.id as first_id,NHA.name as name from nodes_hierarchy NHA join nodes_hierarchy NHB on NHA.parent_id=NHB.id  join nodes_hierarchy NHC on NHC.parent_id=NHA.id where NHB.id={$id} and instr(NHA.name,concat(left(NHB.name,instr(NHB.name,']')-1),'.0]'))<>0 and instr(NHC.name,'0.Sum]')<>0";
  $ret = $dbobj->get_recordset($sql);
  if (count($ret)) {
    $first_id = $ret[0]['first_id'];
    $first_name = $ret[0]['name'];
  }
  $sql = "select NHC.id as last_id,NHA.name as name from nodes_hierarchy NHA join nodes_hierarchy NHB on NHA.parent_id=NHB.id join nodes_hierarchy NHC on NHC.parent_id=NHA.id where NHB.id={$id} and instr(NHA.name,concat(left(NHB.name,instr(NHB.name,']')-1),'.C]'))<>0 and instr(NHC.name,'C.Sum]')<>0";
  $ret = $dbobj->get_recordset($sql);
  if (count($ret)) {
    $last_id = $ret[0]['last_id'];
    $last_name = $ret[0]['name'];
  }
  if ($first_id && $last_id) {
    return array($first_id => $first_name, $last_id => $last_name);
  } else {
    return null;
  }
}
/**
 * Initialize object with information for graphical user interface.
 * 
 * @param tlTestCaseFilterControl $control
 * @return stdClass $gui
 */
function initializeGui(&$dbHandler, &$control)
{
  $gui = new stdClass();
  $gui->feature = $control->args->feature;
  $gui->treeHeader = lang_get('title_navigator') . ' - ' . lang_get('title_test_spec');

  $lblkey = (config_get('testcase_reorder_by') == 'NAME') ? '_alpha' : '_externalid';
  $gui->btn_reorder_testcases = lang_get('btn_reorder_testcases' . $lblkey);

  $feature_path = array(
    'edit_tc' => "lib/testcases/archiveData.php",
    'keywordsAssign' => "lib/keywords/keywordsAssign.php",
    'assignReqs' => "lib/requirements/reqTcAssign.php"
  );

  $gui->tree_drag_and_drop_enabled = array(
    'edit_tc' => (has_rights($dbHandler, "mgt_modify_tc") == 'yes'),
    'keywordsAssign' => false,
    'assignReqs' => false
  );
  $filter_importance = $control->args->filter_importance;
  $filter_execution_type = $control->args->filter_execution_type;
  if (!is_null($filter_importance)) {
    if ($filter_importance != $_SESSION['tcmgr_filter_priority']) {
      $_SESSION['tcmgr_filter_priority'] = $control->args->filter_importance;
    }
  } else {
    $control->filters['filter_importance']['selected'] = $_SESSION['tcmgr_filter_priority'];
  }
  if (!is_null($filter_execution_type)) {
    if ($filter_execution_type != $_SESSION['tcmgr_filter_execution_type']) {
      $_SESSION['tcmgr_filter_execution_type'] = $control->args->filter_execution_type;
    }
  } else {
    $control->filters['filter_execution_type']['selected'] = $_SESSION['tcmgr_filter_execution_type'];
  }


  $gui->menuUrl = $feature_path[$gui->feature];
  return $gui;
}

function a($var)
{
    echo "<xmp class='a-left'>";
    print_r($var);
    echo "</xmp>";
}

function columnNameConvert($colnum) 
{
  
  $num26 = base_convert($colnum, 10, 26);
  $colname = '';
  for ($i = 0; $i < strlen(strval($num26)); $i++) {
    if ($i == 0 && strlen(strval($num26)) != 1) {
      if (is_numeric($num26[$i])) {
        $colname.= chr(ord($num26[$i]) + 16);
      } else {
        $colname.= chr(ord($num26[$i]) - 23);
      }
    } else {
      if (is_numeric($num26[$i])) {
        $colname.= chr(ord($num26[$i]) + 17);
      } else {
        $colname.= chr(ord($num26[$i]) - 22);
      }
    }
  }
  return $colname;
}

function htmlspecialchars_replace($str) 
{
  $str = str_replace('&nbsp;', ' ', $str);
  $str = str_replace('&lt;', '<', $str);
  $str = str_replace('&ldquo;', '"', $str);
  $str = str_replace('&rdquo;', '"', $str);
  $str = str_replace('&quot;', '"', $str);
  $str = str_replace('&times;', 'x', $str);
  return $str;
}